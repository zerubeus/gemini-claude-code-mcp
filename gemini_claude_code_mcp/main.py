"""Main entry point for Gemini-Claude Code MCP server."""

import sys
from typing import Optional

import click
from rich.console import Console

from gemini_claude_code_mcp.mcp_server.server import mcp
from gemini_claude_code_mcp.utils.logging import get_logger, setup_logging

console = Console()


@click.command()
@click.option(
    '--log-level',
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']),
    default='INFO',
    help='Set logging level',
)
@click.option('--log-file', type=click.Path(), default=None, help='Log to file (in addition to console)')
@click.option('--no-rich', is_flag=True, default=False, help='Disable rich console output')
def main(log_level: str, log_file: Optional[str], no_rich: bool):
    """Run the Gemini-Claude Code MCP server."""
    # Set up logging
    setup_logging(level=log_level, log_file=log_file, use_rich=not no_rich)

    logger = get_logger(__name__)

    # Welcome message
    if not no_rich:
        console.print('[bold cyan]🚀 Gemini-Claude Code MCP Server[/bold cyan]', justify='center')
        console.print("Bridging Claude Code with Google Gemini's massive context window", justify='center', style='dim')
        console.print()

    logger.info(
        'Starting Gemini-Claude Code MCP server', log_level=log_level, log_file=log_file, rich_output=not no_rich
    )

    try:
        # Run the FastMCP server
        mcp.run()
    except KeyboardInterrupt:
        logger.info('Server stopped by user')
        if not no_rich:
            console.print('\n[yellow]Server stopped by user[/yellow]')
    except Exception as e:
        logger.error('Server error', error=str(e), exc_info=True)
        if not no_rich:
            console.print(f'\n[red]Server error: {e}[/red]')
        sys.exit(1)


if __name__ == '__main__':
    main()
