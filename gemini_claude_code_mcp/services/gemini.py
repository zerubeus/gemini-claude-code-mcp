from google import genai

from gemini_claude_code_mcp.config.settings import settings


def get_gemini_client():
    """Create and return a Google Gemini API client."""
    return genai.Client(api_key=settings.gemini.api_key)
