# Character Image Generation

## Current Status

✅ **The image generation feature is now fully functional** using Google's **Gemini 2.5 Flash Image** model through LangChain integration.

## What's Implemented

The codebase has **full support** for character image generation, including:

- ✅ **Parallel image generation** with semaphore-based rate limiting
- ✅ **Async HTTP calls** to Gemini API using aiohttp
- ✅ **Exponential backoff retry logic** for handling rate limits
- ✅ **Image embedding in PDFs** (character sheets)
- ✅ **Detailed prompt generation** with cultural and period context
- ✅ **Mock mode** for testing without API calls
- ✅ **Graceful fallback** when API is unavailable

## How It Works

The implementation uses **Gemini 2.5 Flash Image** through LangChain:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash-image",
    temperature=0.6,
    google_api_key=os.environ["GOOGLE_API_KEY"],
)

message = HumanMessage(
    content=[{"type": "text", "text": "Your detailed character prompt here"}]
)

resp = llm.invoke(
    [message],
    generation_config={"response_modalities": ["IMAGE"]}
)

# Extract and save image
img_b64 = resp.content[0].get("image_url")["url"].split(",")[-1]
img_data = base64.b64decode(img_b64)
image = Image.open(BytesIO(img_data))
image.save("character.png")
```

## How to Enable

Simply run with the flag:

```bash
uv run mystery-agents --generate-images
```

The system will:
1. Warn you about API costs
2. Request confirmation
3. Generate images in parallel with rate limiting
4. Embed them in character sheet PDFs

## Alternative Solutions

### Option 1: Vertex AI (Enterprise)

If you have a Google Cloud project with Vertex AI access:

1. Set up Vertex AI credentials
2. Modify `_call_gemini_image_api()` to use Vertex AI SDK:
   ```python
   from google.cloud import aiplatform
   # Use Vertex AI's Imagen endpoint
   ```

### Option 2: Other Image Generation Services

You can integrate alternative services:

#### DALL-E 3 (OpenAI)
```python
from openai import OpenAI
client = OpenAI()
response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
)
```

#### Stable Diffusion (via Stability AI)
```python
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from stability_sdk import client

stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'],
    engine="stable-diffusion-xl-1024-v1-0",
)
```

### Option 3: Manual Image Addition

1. Generate images using any tool (Midjourney, DALL-E, etc.)
2. Save them as: `output/game_xxxxx/images/characters/char_001_name.png`
3. Update character `image_path` field manually
4. Regenerate PDFs

## Technical Details

### Code Structure

**Agent**: `src/mystery_agents/agents/a3_5_character_images.py`
- Handles parallel generation with semaphore
- Rate limiting: 5 concurrent requests
- Retry logic: 3 attempts with exponential backoff

**Workflow Integration**: `src/mystery_agents/graph/workflow.py`
- Node `a3_5_character_images` between A3 (characters) and A4 (relationships)
- Graceful error handling
- Continues game generation even if images fail

**PDF Integration**: `src/mystery_agents/agents/a9_packaging.py`
- Embeds images in character sheet markdown
- WeasyPrint renders images in PDFs
- Relative path resolution for proper display

### Prompt Template

The system generates detailed prompts including:
- Character name, age, gender, role
- Personality traits
- Historical period and cultural context
- Costume details
- Visual style requirements (photorealistic, period-appropriate)

Example prompt:
```
Generate a photorealistic portrait of a female character for a mystery party game.

CHARACTER DETAILS:
- Name: Elena Martínez
- Age: 30-35
- Role: Detective
- Description: Sharp and observant
- Personality: clever, skeptical, determined

SETTING CONTEXT:
- Historical Period: 1930s
- Location: Family mansion in Las Palmas
- Country/Culture: Spain

STYLE REQUIREMENTS:
- Photorealistic, professional portrait
- 1930s-era fashion appropriate for Spain
- Formal mystery party atmosphere
- Dramatic, film noir lighting
```

## Future Improvements

When the API becomes available, potential enhancements:

1. **Character consistency**: Use reference images to maintain consistent appearance
2. **Style selection**: Allow users to choose art styles (photorealistic, illustrated, etc.)
3. **Batch optimization**: Further optimize parallel requests
4. **Local caching**: Cache generated images to avoid regeneration
5. **Image upscaling**: Enhance resolution for print quality

## Questions?

If you have information about Imagen API availability or want to contribute an integration with an alternative service, please open an issue or PR.

## Related Files

- `src/mystery_agents/agents/a3_5_character_images.py` - Main implementation
- `src/mystery_agents/graph/workflow.py` - Workflow integration
- `src/mystery_agents/agents/a9_packaging.py` - PDF embedding
- `src/mystery_agents/utils/pdf_generator.py` - PDF rendering with images
- `tests/unit/test_character_image_agent.py` - Unit tests

