"""
AMP Envelope tools for controlling AMP EG parameters on the Moog Sub 37.
"""

from mcp.server.fastmcp import FastMCP

from moog_sub37_mcp.midi.midi_manager import MIDIManager


def register_amp_tools(mcp: FastMCP, midi: MIDIManager):
    """
    Register all AMP envelope tools with the MCP server.

    Args:
        mcp: The MCP server instance
        midi: The MIDI interface
    """

    @mcp.tool()
    def set_amp_eg_attack_time(value: int, channel: int = 3):  # type: ignore
        """
        Set the AMP EG Attack Time with high resolution.

        Args:
            value (int): High-resolution value for AMP EG Attack Time (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 28, 60, value)

    @mcp.tool()
    def set_amp_eg_decay_time(value: int, channel: int = 3):  # type: ignore
        """
        Set the AMP EG Decay Time with high resolution.

        Args:
            value (int): High-resolution value for AMP EG Decay Time (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 29, 61, value)

    @mcp.tool()
    def set_amp_eg_sustain_time(value: int, channel: int = 3):  # type: ignore
        """
        Set the AMP EG Sustain Time with high resolution.

        Args:
            value (int): High-resolution value for AMP EG Sustain Time (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 30, 62, value)

    @mcp.tool()
    def set_amp_eg_release_time(value: int, channel: int = 3):  # type: ignore
        """
        Set the AMP EG Release Time with high resolution.

        Args:
            value (int): High-resolution value for AMP EG Release Time (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 31, 63, value)

    @mcp.tool()
    def set_amp_eg_hold(value: int, channel: int = 3):  # type: ignore
        """
        Set the AMP EG Hold.

        Args:
            value (int): Value for AMP EG Hold (0-127).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 106, value)

    @mcp.tool()
    def set_amp_eg_multi_trig(value: int, channel: int = 3):  # type: ignore
        """
        Set the AMP EG Multi Trigger.

        Args:
            value (int): Value for AMP EG Multi Trigger (0 = OFF, 64 = ON).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 113, value)
