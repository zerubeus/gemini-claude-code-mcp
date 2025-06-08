"""
MCP server configuration and initialization.
"""

from mcp.server.fastmcp import FastMCP

from moog_sub37_mcp.midi.midi_manager import MIDIManager
from moog_sub37_mcp.tools.amp_tool import register_amp_tools
from moog_sub37_mcp.tools.arp_tool import register_arp_tools
from moog_sub37_mcp.tools.filter_tool import register_filter_tools
from moog_sub37_mcp.tools.fx_tool import register_fx_tools
from moog_sub37_mcp.tools.glide_tool import register_glide_tools
from moog_sub37_mcp.tools.global_tool import register_global_tools
from moog_sub37_mcp.tools.lfo_tool import register_lfo_tools
from moog_sub37_mcp.tools.mod_tool import register_mod_tools
from moog_sub37_mcp.tools.osc_tool import register_osc_tools

# Initialize MCP and MIDI
mcp = FastMCP('Moog Sub 37')
midi = MIDIManager('Moog Sub 37')

# Register all tools
register_arp_tools(mcp, midi)
register_global_tools(mcp, midi)
register_mod_tools(mcp, midi)
register_osc_tools(mcp, midi)
register_lfo_tools(mcp, midi)
register_fx_tools(mcp, midi)
register_amp_tools(mcp, midi)
register_filter_tools(mcp, midi)
register_glide_tools(mcp, midi)

# Export the configured MCP server
__all__ = ['mcp']
