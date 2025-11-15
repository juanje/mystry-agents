"""Character Image Generation Agent (A3.5) with parallel processing."""

from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path

from langchain_core.language_models import BaseChatModel

from mystery_agents.agents.base import BaseAgent
from mystery_agents.models.state import CharacterSpec, GameState
from mystery_agents.utils.state_helpers import (
    safe_get_world_epoch,
    safe_get_world_location_name,
)

logger = logging.getLogger(__name__)


class CharacterImageAgent(BaseAgent):
    """
    Agent that generates character portrait images using Gemini Image API.

    Features:
    - Parallel image generation with rate limiting (respects Gemini API limits)
    - Semaphore-based concurrency control
    - Exponential backoff for rate limit errors
    - Mock generation in dry-run mode
    """

    MAX_CONCURRENT_REQUESTS = 5  # Safe limit under Gemini's 10 RPM for Imagen 4 Fast
    MAX_RETRIES = 3
    RETRY_DELAY_BASE = 2.0  # Exponential backoff starting delay

    def __init__(self, llm: BaseChatModel | None = None) -> None:
        """
        Initialize the character image generation agent.

        Args:
            llm: The language model (not used for image generation,
                 optional for compatibility with base class)
        """
        # Image generation doesn't use LLM, so we create a dummy one if not provided
        from mystery_agents.utils.cache import LLMCache

        if llm is None:
            llm = LLMCache.get_model("tier3")  # Cheapest tier, won't be used anyway

        super().__init__(llm, response_format=None)

    def get_system_prompt(self, state: GameState) -> str:
        """
        Not used for image generation.

        Args:
            state: Current game state

        Returns:
            Empty string (not applicable for image generation)
        """
        return ""

    def run(self, state: GameState) -> GameState:
        """
        Generate character images in parallel with rate limiting.

        Args:
            state: Current game state with characters

        Returns:
            Updated state with image_path populated for each character
        """
        # Skip if image generation is not enabled
        if not state.config.generate_images:
            logger.info("[A3.5] ⊘ Image generation disabled, skipping")
            return state

        if self._should_use_mock(state):
            logger.info("[A3.5] 🎭 Character Images: Dry run mode - using mocks")
            return self._mock_output(state)

        if not state.characters:
            logger.warning("[A3.5] ⚠️  No characters found, skipping image generation")
            return state

        logger.info(
            f"[A3.5] 🎨 Generating {len(state.characters)} character images in parallel "
            f"(max {self.MAX_CONCURRENT_REQUESTS} concurrent)"
        )

        # Create output directory for images
        output_dir = self._get_image_output_dir(state)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate images in parallel using asyncio
        asyncio.run(self._generate_all_images(state, output_dir))

        # Log success with paths for debugging
        images_with_paths = 0
        for char in state.characters:
            if char.image_path:
                logger.info(f"[A3.5] 📸 {char.name}: {char.image_path}")
                images_with_paths += 1
            else:
                logger.warning(f"[A3.5] ⚠️  {char.name}: No image path set")

        logger.info(
            f"[A3.5] ✅ All character images generated in {output_dir} "
            f"({images_with_paths}/{len(state.characters)} with paths)"
        )

        # Return updated state with modified characters
        # This ensures LangGraph sees the changes
        return state.model_copy(update={"characters": state.characters})

    async def _generate_all_images(self, state: GameState, output_dir: Path) -> None:
        """
        Generate all character images in parallel with concurrency control.

        Args:
            state: Current game state
            output_dir: Directory to save images
        """
        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(self.MAX_CONCURRENT_REQUESTS)

        # Create tasks for all characters
        tasks = [
            self._generate_character_image_with_semaphore(character, state, output_dir, semaphore)
            for character in state.characters
        ]

        # Wait for all images to be generated
        await asyncio.gather(*tasks)

    async def _generate_character_image_with_semaphore(
        self,
        character: CharacterSpec,
        state: GameState,
        output_dir: Path,
        semaphore: asyncio.Semaphore,
    ) -> None:
        """
        Generate a single character image with semaphore-based rate limiting.

        Args:
            character: Character specification
            state: Current game state
            output_dir: Directory to save image
            semaphore: Asyncio semaphore for concurrency control
        """
        async with semaphore:
            await self._generate_character_image(character, state, output_dir)

    async def _generate_character_image(
        self, character: CharacterSpec, state: GameState, output_dir: Path
    ) -> None:
        """
        Generate image for a single character with retry logic.

        Args:
            character: Character specification
            state: Current game state
            output_dir: Directory to save image
        """
        prompt = self._build_image_prompt(character, state)
        image_filename = f"{character.id}_{character.name.lower().replace(' ', '_')}.png"
        image_path = output_dir / image_filename

        for attempt in range(self.MAX_RETRIES):
            try:
                logger.info(
                    f"[A3.5] 🎨 Generating image for {character.name} "
                    f"(attempt {attempt + 1}/{self.MAX_RETRIES})"
                )

                # Call Gemini Image API
                await self._call_gemini_image_api(prompt, image_path)

                # Update character with image path (absolute path for robustness)
                character.image_path = str(image_path.absolute())

                logger.info(f"[A3.5] ✅ Generated: {character.name} -> {image_path.name}")
                return

            except Exception as e:
                if attempt < self.MAX_RETRIES - 1:
                    delay = self.RETRY_DELAY_BASE * (2**attempt)
                    logger.warning(
                        f"[A3.5] ⚠️  Error generating image for {character.name}: {e}. "
                        f"Retrying in {delay}s..."
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(
                        f"[A3.5] ❌ Failed to generate image for {character.name} "
                        f"after {self.MAX_RETRIES} attempts: {e}"
                    )
                    # Don't fail the entire generation, just skip this image
                    character.image_path = None

    async def _call_gemini_image_api(self, prompt: str, output_path: Path) -> None:
        """
        Call Gemini Image Generation API using Gemini 2.5 Flash Image model.

        Uses LangChain's ChatGoogleGenerativeAI with response_modalities=["IMAGE"]
        to generate images from text prompts.

        Args:
            prompt: Image generation prompt
            output_path: Where to save the generated image

        Raises:
            Exception: If image generation fails
        """
        try:
            import base64
            from io import BytesIO

            from langchain_core.messages import HumanMessage
            from langchain_google_genai import ChatGoogleGenerativeAI
            from PIL import Image as PILImage

            # Get API key
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not set")

            # Initialize Gemini 2.5 Flash Image model
            llm = ChatGoogleGenerativeAI(
                model="models/gemini-2.5-flash-image",
                temperature=0.6,
                google_api_key=api_key,
            )

            # Create message with image generation prompt
            message = HumanMessage(content=[{"type": "text", "text": prompt}])

            # Generate image with IMAGE response modality
            # Run in executor to make it async-compatible
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(
                None,
                lambda: llm.invoke([message], generation_config={"response_modalities": ["IMAGE"]}),
            )

            # Extract base64 image data from response
            # resp.content is a list, first element should be a dict with image_url
            content_item = resp.content[0]
            if not isinstance(content_item, dict):
                raise ValueError(
                    f"Unexpected response format: content[0] is {type(content_item)}, expected dict"
                )

            image_url_data = content_item.get("image_url")
            if not image_url_data or not isinstance(image_url_data, dict):
                raise ValueError(f"No image_url found in response: {content_item}")

            url_str = image_url_data.get("url")
            if not url_str or not isinstance(url_str, str):
                raise ValueError(f"No valid URL string in image_url: {image_url_data}")

            # Extract base64 data (format: data:image/png;base64,<data>)
            img_b64 = url_str.split(",")[-1]
            img_data = base64.b64decode(img_b64)

            # Open and save image
            image = PILImage.open(BytesIO(img_data))
            image.save(str(output_path), "PNG")

            logger.info(f"[A3.5] 📸 Image saved to {output_path.name}")

        except ImportError as e:
            logger.error(
                f"[A3.5] ❌ Missing dependencies for image generation: {e}. "
                "Run: uv sync to install required packages"
            )
            raise
        except Exception as e:
            logger.error(f"[A3.5] ❌ Image generation failed: {e}")
            raise

    def _build_image_prompt(self, character: CharacterSpec, state: GameState) -> str:
        """
        Build a detailed image generation prompt for a character.

        Args:
            character: Character specification
            state: Current game state

        Returns:
            Detailed prompt for image generation
        """
        # Get world context
        epoch = safe_get_world_epoch(state)
        location = safe_get_world_location_name(state)
        country = state.config.country if state.config else "Unknown"

        # Build detailed prompt
        personality = (
            ", ".join(character.personality_traits)
            if character.personality_traits
            else "mysterious"
        )

        prompt = f"""Generate a photorealistic portrait of a {character.gender} character for a mystery party game.

CHARACTER DETAILS:
- Name: {character.name}
- Age: {character.age_range}
- Role: {character.role}
- Description: {character.public_description}
- Personality: {personality}

SETTING CONTEXT:
- Historical Period: {epoch}
- Location: {location}
- Country/Culture: {country}

COSTUME:
{character.costume_suggestion if character.costume_suggestion else f"Period-appropriate attire for {epoch} in {country}"}

STYLE REQUIREMENTS:
- Photorealistic, professional portrait
- {epoch}-era fashion and styling appropriate for {country}
- Formal mystery party atmosphere
- High-quality, 8K resolution
- Lighting: Dramatic, film noir style
- Framing: Head and shoulders portrait
- Background: Subtle, period-appropriate
- Expression: {personality} demeanor

The image should feel like a character from a high-quality period mystery film."""

        return prompt

    def _get_image_output_dir(self, state: GameState) -> Path:
        """
        Get the output directory for character images.

        Args:
            state: Current game state

        Returns:
            Path to images directory
        """
        # Use game_id from meta
        game_id = state.meta.id[:8] if state.meta else "default"
        base_dir = Path("output") / f"game_{game_id}"

        return base_dir / "images" / "characters"

    def _mock_output(self, state: GameState) -> GameState:
        """
        Generate mock image paths for dry run mode.

        Args:
            state: Current game state

        Returns:
            State with mock image paths
        """
        output_dir = self._get_image_output_dir(state)

        for character in state.characters:
            mock_filename = f"{character.id}_{character.name.lower().replace(' ', '_')}.png"
            character.image_path = str((output_dir / mock_filename).absolute())
            logger.info(f"[A3.5] 🎭 Mock image: {character.name} -> {mock_filename}")

        return state
