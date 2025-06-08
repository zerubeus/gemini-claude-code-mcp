"""
ARP tools for controlling arpeggiator parameters on the Moog Sub 37.
"""

from mcp.server.fastmcp import FastMCP

from moog_sub37_mcp.midi.midi_manager import MIDIManager


def register_arp_tools(mcp: FastMCP, midi: MIDIManager):
    """
    Register all ARP tools with the MCP server.

    Args:
        mcp: The MCP server instance
        midi: The MIDI interface
    """

    @mcp.tool()
    def set_arp_rate(value: int, channel: int = 3):  # type: ignore
        """
        Set the ARP Rate (NRPN 403, MSB 3, LSB 19).
        Args:
            value (int): Value for ARP Rate (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 19, value)

    @mcp.tool()
    def set_arp_sync(value: int, channel: int = 3):  # type: ignore
        """
        Set the ARP Sync (NRPN 404, MSB 3, LSB 20).
        Args:
            value (int): Value for ARP Sync (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 20, value)

    @mcp.tool()
    def set_arp_range(value: int, channel: int = 3):  # type: ignore
        """
        Set the ARP Range (NRPN 405, MSB 3, LSB 21).
        Args:
            value (int): Value for ARP Range (0-6).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 21, value)

    @mcp.tool()
    def set_arp_back_forth(value: int, channel: int = 3):  # type: ignore
        """
        Set the ARP Back Forth (NRPN 406, MSB 3, LSB 22).
        Args:
            value (int): Value for ARP Back Forth (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 22, value)

    @mcp.tool()
    def set_arp_bf_mode(value: int, channel: int = 3):  # type: ignore
        """
        Set the ARP BF Mode (NRPN 407, MSB 3, LSB 23).
        Args:
            value (int): Value for ARP BF Mode (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 23, value)

    @mcp.tool()
    def set_arp_invert(value: int, channel: int = 3):  # type: ignore
        """
        Set the ARP Invert (NRPN 408, MSB 3, LSB 24).
        Args:
            value (int): Value for ARP Invert (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 24, value)

    @mcp.tool()
    def set_arp_pattern(value: int, channel: int = 3):  # type: ignore
        """
        Set the ARP Pattern (NRPN 409, MSB 3, LSB 25).
        Args:
            value (int): Value for ARP Pattern (0-5).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 25, value)

    @mcp.tool()
    def set_arp_run(value: int, channel: int = 3):  # type: ignore
        """
        Set the ARP Run (NRPN 410, MSB 3, LSB 26).
        Args:
            value (int): Value for ARP Run (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 26, value)

    @mcp.tool()
    def set_arp_latch(value: int, channel: int = 3):  # type: ignore
        """
        Set the ARP Latch (NRPN 411, MSB 3, LSB 27).
        Args:
            value (int): Value for ARP Latch (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 27, value)

    @mcp.tool()
    def set_arp_gate_len(value: int, channel: int = 3):  # type: ignore
        """
        Set the ARP Gate Length (NRPN 412, MSB 3, LSB 28).
        Args:
            value (int): Value for ARP Gate Length (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 28, value)

    @mcp.tool()
    def set_arp_clk_div(value: int, channel: int = 3):  # type: ignore
        """
        Set the ARP Clock Divider (NRPN 413, MSB 3, LSB 29).
        Args:
            value (int): Value for ARP Clock Divider (0-20).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 29, value)

    @mcp.tool()
    def set_arp_step1_reset(value: int, channel: int = 3):  # type: ignore
        """
        Set the ARP Step 1 Reset (NRPN 416, MSB 3, LSB 32).
        Args:
            value (int): Value for ARP Step 1 Reset (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 32, value)
