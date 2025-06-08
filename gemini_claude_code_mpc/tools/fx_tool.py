"""
FX and Misc tools for controlling FX, arpeggiator, and other parameters on the Moog Sub 37.
"""

from mcp.server.fastmcp import FastMCP

from moog_sub37_mcp.midi.midi_manager import MIDIManager


def register_fx_tools(mcp: FastMCP, midi: MIDIManager):
    """
    Register all FX, arpeggiator, and misc tools with the MCP server.

    Args:
        mcp: The MCP server instance
        midi: The MIDI interface
    """

    @mcp.tool()
    def set_hold_pedal(value: int, channel: int = 3):  # type: ignore
        """
        Set the Hold Pedal/Sustain.

        Args:
            value (int): Value for Hold Pedal (0 = OFF, 64 = ON).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 64, value)

    @mcp.tool()
    def set_glide(value: int, channel: int = 3):  # type: ignore
        """
        Set the Glide On/Off.

        Args:
            value (int): Value for Glide (0 = OFF, 64 = ON).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 65, value)

    @mcp.tool()
    def set_arpeggiator_latch(value: int, channel: int = 3):  # type: ignore
        """
        Set the Arpeggiator Latch.

        Args:
            value (int): Value for Arpeggiator Latch (0 = OFF, 64 = ON).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 69, value)

    @mcp.tool()
    def set_arp_on_off(value: int, channel: int = 3):  # type: ignore
        """
        Set the Arpeggiator On/Off.

        Args:
            value (int): Value for Arpeggiator (0 = OFF, 64 = ON).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 73, value)

    @mcp.tool()
    def set_glide_dest_osc(value: int, channel: int = 3):  # type: ignore
        """
        Set the Glide Destination OSC 1/2/BOTH.

        Args:
            value (int): Value for Glide Destination (0 = OSC1 + OSC2, 43 = OSC1, 85 = OSC2).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 102, value)

    @mcp.tool()
    def set_filter_eg_multi_trig(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter EG Multi Trig.

        Args:
            value (int): Value for Filter EG Multi Trig (0 = OFF, 64 = ON).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 112, value)
