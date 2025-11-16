"""Host Character Image Generation Agent (A8.5) - Generates victim and detective images."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

from langchain_core.language_models import BaseChatModel

from mystery_agents.agents.base import BaseAgent
from mystery_agents.models.state import DetectiveRole, GameState, VictimSpec
from mystery_agents.utils.state_helpers import (
    safe_get_world_epoch,
    safe_get_world_location_name,
)


class HostImageAgent(BaseAgent):
    """
    Agent that generates character portrait images for host characters (victim and detective).

    Features:
    - Generates images for victim (Act 1) and detective (Act 2)
    - Same technology as CharacterImageAgent (Gemini Image API)
    - Exponential backoff for rate limit errors
    - Mock generation in dry-run mode
    """

    MAX_RETRIES = 3
    RETRY_DELAY_BASE = 2.0  # Exponential backoff starting delay

    def __init__(self, llm: BaseChatModel | None = None) -> None:
        """
        Initialize the host image generation agent.

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
        Generate host character images (victim and detective).

        Args:
            state: Current game state with crime (victim) and host_guide (detective)

        Returns:
            Updated state with image_path populated for victim and detective
        """
        # Skip if image generation is not enabled
        if not state.config.generate_images:
            return state

        if self._should_use_mock(state):
            return self._mock_output(state)

        # Check if we have victim and detective
        has_victim = state.crime and state.crime.victim
        has_detective = state.host_guide and state.host_guide.host_act2_detective_role

        if not has_victim and not has_detective:
            return state

        # Create output directory for images
        output_dir = self._get_image_output_dir(state)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate images sequentially (only 2 images, no need for parallelization)
        asyncio.run(self._generate_host_images(state, output_dir))

        # Return updated state
        return state

    async def _generate_host_images(self, state: GameState, output_dir: Path) -> None:
        """
        Generate images for victim and detective.

        Args:
            state: Current game state
            output_dir: Directory to save images
        """
        # Generate victim image
        if state.crime and state.crime.victim:
            await self._generate_victim_image(state.crime.victim, state, output_dir)

        # Generate detective image
        if state.host_guide and state.host_guide.host_act2_detective_role:
            await self._generate_detective_image(
                state.host_guide.host_act2_detective_role, state, output_dir
            )

    async def _generate_victim_image(
        self, victim: VictimSpec, state: GameState, output_dir: Path
    ) -> None:
        """
        Generate image for the victim character.

        Args:
            victim: Victim specification
            state: Current game state
            output_dir: Directory to save image
        """
        prompt = self._build_victim_image_prompt(victim, state)
        image_filename = f"{victim.id}_{victim.name.lower().replace(' ', '_')}.png"
        image_path = output_dir / image_filename

        for attempt in range(self.MAX_RETRIES):
            try:
                # Call Gemini Image API
                await self._call_gemini_image_api(prompt, image_path)

                # Update victim with image path (absolute path for robustness)
                victim.image_path = str(image_path.absolute())
                return

            except Exception:
                if attempt < self.MAX_RETRIES - 1:
                    delay = self.RETRY_DELAY_BASE * (2**attempt)
                    await asyncio.sleep(delay)
                else:
                    # Don't fail the entire generation, just skip this image
                    victim.image_path = None

    async def _generate_detective_image(
        self, detective: DetectiveRole, state: GameState, output_dir: Path
    ) -> None:
        """
        Generate image for the detective character.

        Args:
            detective: Detective role specification
            state: Current game state
            output_dir: Directory to save image
        """
        prompt = self._build_detective_image_prompt(detective, state)
        # Use a unique ID for detective
        detective_id = f"detective-{state.meta.id[:8]}"
        image_filename = f"{detective_id}_{detective.character_name.lower().replace(' ', '_')}.png"
        image_path = output_dir / image_filename

        for attempt in range(self.MAX_RETRIES):
            try:
                # Call Gemini Image API
                await self._call_gemini_image_api(prompt, image_path)

                # Update detective with image path (absolute path for robustness)
                detective.image_path = str(image_path.absolute())
                return

            except Exception:
                if attempt < self.MAX_RETRIES - 1:
                    delay = self.RETRY_DELAY_BASE * (2**attempt)
                    await asyncio.sleep(delay)
                else:
                    # Don't fail the entire generation, just skip this image
                    detective.image_path = None

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

        except Exception:
            raise

    def _build_victim_image_prompt(self, victim: VictimSpec, state: GameState) -> str:
        """
        Build a detailed image generation prompt for the victim character.

        Args:
            victim: Victim specification
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
            ", ".join(victim.personality_traits)
            if victim.personality_traits
            else "mysterious, commanding"
        )

        prompt = f"""Generate a photorealistic portrait of a {victim.gender} character for a mystery party game.

CHARACTER DETAILS:
- Name: {victim.name}
- Age: {victim.age}
- Role: {victim.role_in_setting}
- Description: {victim.public_persona}
- Personality: {personality}
- Context: This is the VICTIM of the mystery - a central figure who will be murdered

SETTING CONTEXT:
- Historical Period: {epoch}
- Location: {location}
- Country/Culture: {country}

COSTUME:
{victim.costume_suggestion if victim.costume_suggestion else f"Period-appropriate formal attire for {epoch} in {country}"}

STYLE REQUIREMENTS:
- Photorealistic, professional portrait
- {epoch}-era fashion and styling appropriate for {country}
- Formal, authoritative presence (this is a central character)
- High-quality, 8K resolution
- Lighting: Dramatic, film noir style
- Framing: Head and shoulders portrait
- Background: Elegant, period-appropriate setting
- Expression: {personality} demeanor, commanding presence

The image should feel like a character from a high-quality period mystery film - someone important enough to be the center of the story."""

        return prompt

    def _build_detective_image_prompt(self, detective: DetectiveRole, state: GameState) -> str:
        """
        Build a detailed image generation prompt for the detective character.

        Args:
            detective: Detective role specification
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
            ", ".join(detective.personality_traits)
            if detective.personality_traits
            else "analytical, observant, methodical"
        )

        prompt = f"""Generate a photorealistic portrait of a detective character for a mystery party game.

CHARACTER DETAILS:
- Name: {detective.character_name}
- Role: Detective investigating the murder
- Description: {detective.public_description}
- Personality: {personality}
- Context: This is the DETECTIVE who will solve the mystery in Act 2

SETTING CONTEXT:
- Historical Period: {epoch}
- Location: {location}
- Country/Culture: {country}

COSTUME:
{detective.costume_suggestion if detective.costume_suggestion else f"Classic detective attire for {epoch} in {country}"}

STYLE REQUIREMENTS:
- Photorealistic, professional portrait
- {epoch}-era detective fashion and styling appropriate for {country}
- Sharp, intelligent, investigative presence
- High-quality, 8K resolution
- Lighting: Dramatic, film noir style with slight edge lighting
- Framing: Head and shoulders portrait
- Background: Subtle, atmospheric setting suggesting investigation
- Expression: {personality} demeanor, sharp gaze, intelligent look

The image should feel like a classic detective from a high-quality period mystery film - someone perceptive and methodical."""

        return prompt

    def _get_image_output_dir(self, state: GameState) -> Path:
        """
        Get the output directory for host character images.

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

        # Mock victim image
        if state.crime and state.crime.victim:
            victim = state.crime.victim
            mock_filename = f"{victim.id}_{victim.name.lower().replace(' ', '_')}.png"
            victim.image_path = str((output_dir / mock_filename).absolute())

        # Mock detective image
        if state.host_guide and state.host_guide.host_act2_detective_role:
            detective = state.host_guide.host_act2_detective_role
            detective_id = f"detective-{state.meta.id[:8]}"
            mock_filename = (
                f"{detective_id}_{detective.character_name.lower().replace(' ', '_')}.png"
            )
            detective.image_path = str((output_dir / mock_filename).absolute())

        return state
