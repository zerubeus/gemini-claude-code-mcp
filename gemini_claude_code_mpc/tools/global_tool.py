"""
Global and utility tools for controlling global parameters on the Moog Sub 37.
"""

from mcp.server.fastmcp import FastMCP

from moog_sub37_mcp.midi.midi_manager import MIDIManager


def register_global_tools(mcp: FastMCP, midi: MIDIManager):
    """
    Register all global and utility tools with the MCP server.

    Args:
        mcp: The MCP server instance
        midi: The MIDI interface
    """

    @mcp.tool()
    def set_mod_wheel(value: int, channel: int = 3):  # type: ignore
        """
        Set the Mod Wheel (normal resolution).

        Args:
            value (int): Value for Mod Wheel (0-127).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 1, value)

    @mcp.tool()
    def set_mod_wheel_high_res(value: int, channel: int = 3):  # type: ignore
        """
        Set the Mod Wheel (high resolution).

        Args:
            value (int): High-resolution value for Mod Wheel (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 1, 33, value)

    @mcp.tool()
    def set_bank_select(value: int, channel: int = 3):  # type: ignore
        """
        Set the Bank Select (MSB).

        Args:
            value (int): Value for Bank Select (should always be 0).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 0, value)

    @mcp.tool()
    def set_bank_select_lsb(value: int, channel: int = 3):  # type: ignore
        """
        Set the Bank Select (LSB).

        Args:
            value (int): Value for Bank Select LSB (0 = Banks 1–8, 1 = Banks 9–16).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 32, value)

    @mcp.tool()
    def set_kb_octave(value: int, channel: int = 3):  # type: ignore
        """
        Set the Keyboard Octave.

        Args:
            value (int): Value for Keyboard Octave (0 = -2 Oct, 26 = -1 Oct, 51 = +0 Oct, 77 = +1 Oct, 102 = +2 Oct).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 89, value)

    @mcp.tool()
    def set_local_control(value: int, channel: int = 3):  # type: ignore
        """
        Set Local Control On/Off.

        Args:
            value (int): Value for Local Control (0 = OFF, 127 = ON).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 122, value)

    @mcp.tool()
    def set_master_volume(value: int, channel: int = 3):  # type: ignore
        """
        Set the Master Volume (normal resolution).

        Args:
            value (int): Value for Master Volume (0-127).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 7, value)

    @mcp.tool()
    def set_master_volume_high_res(value: int, channel: int = 3):  # type: ignore
        """
        Set the Master Volume (high resolution).

        Args:
            value (int): High-resolution value for Master Volume (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 7, 39, value)

    @mcp.tool()
    def set_kb_transpose(value: int, channel: int = 3):  # type: ignore
        """
        Set the Keyboard Transpose.

        Args:
            value (int): Value for Keyboard Transpose (-12 to +13 semitones, receive only).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 119, value)

    @mcp.tool()
    def all_notes_off(channel: int = 3):  # type: ignore
        """
        Send All Notes Off message.

        Args:
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 123, 0)
