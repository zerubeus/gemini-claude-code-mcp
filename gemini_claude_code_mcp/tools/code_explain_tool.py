"""AMP Envelope tools for controlling AMP EG parameters on the Moog Sub 37."""

from typing import Any

from fastmcp import FastMCP


def register_code_explain_tools(mcp: FastMCP[Any]):
    """Register all tools related to code explanation and documentation generation."""

    @mcp.tool()
    def generate_doc_for_specific_folder(absolute_folder_path: str, prompt: str = 'Generate documentation'):  # type: ignore
        """Generate documentation for a specific folder.

        Args:
            absolute_folder_path (str): The absolute folder path to generate documentation for.
            prompt (str): The prompt to use. Defaults to "Generate documentation".

        """
        pass
