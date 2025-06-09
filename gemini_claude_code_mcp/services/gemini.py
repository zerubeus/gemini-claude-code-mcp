# sdk doc can be found at: https://googleapis.github.io/python-genai/

from google import genai
from google.genai import types

from gemini_claude_code_mcp.config.settings import settings

gemini_client = genai.Client(api_key=settings.gemini.api_key)


async def gemini_text_to_text(
    prompt: str,
    system_instruction: list[str] | None = None,
    model: str = settings.gemini.model,
    temperature: float = settings.gemini.temperature,
    max_output_tokens: int = settings.gemini.max_output_tokens,
) -> str | None:
    """Generate text using Gemini's text-to-text model."""
    contents = [types.Content(role='user', parts=[types.Part.from_text(text=prompt)])]

    generate_content_config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        response_mime_type='text/plain',
    )

    response = await gemini_client.aio.models.generate_content(  # type: ignore[attr-defined]
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    return response.text
