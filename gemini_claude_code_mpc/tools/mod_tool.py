"""
MOD tools for controlling modulation parameters on the Moog Sub 37.
"""

from mcp.server.fastmcp import FastMCP

from moog_sub37_mcp.midi.midi_manager import MIDIManager


def register_mod_tools(mcp: FastMCP, midi: MIDIManager):
    """
    Register all MOD tools with the MCP server.

    Args:
        mcp: The MCP server instance
        midi: The MIDI interface
    """

    @mcp.tool()
    def set_mod1_mwhl_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 MWHL AMT (NRPN 435, MSB 3, LSB 51).
        Args:
            value (int): Value for MOD 1 MWHL AMT (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 51, value)

    @mcp.tool()
    def set_mod1_velocity_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 VELOCITY AMT (NRPN 436, MSB 3, LSB 52).
        Args:
            value (int): Value for MOD 1 VELOCITY AMT (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 52, value)

    @mcp.tool()
    def set_mod1_pressure_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 PRESSURE AMT (NRPN 437, MSB 3, LSB 53).
        Args:
            value (int): Value for MOD 1 PRESSURE AMT (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 53, value)

    @mcp.tool()
    def set_mod1_ctl4_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 CTL4 AMT (NRPN 438, MSB 3, LSB 54).
        Args:
            value (int): Value for MOD 1 CTL4 AMT (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 54, value)

    @mcp.tool()
    def set_mod1_source(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 SOURCE (NRPN 440, MSB 3, LSB 56).
        Args:
            value (int): Value for MOD 1 SOURCE (0-6):
                0 = TRIANGLE LFO
                1 = SQUARE LFO
                2 = SAW LFO
                3 = RAMP LFO
                4 = S&H LFO
                5 = F.EG/PGM
                6 = Reserved
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 56, value)

    @mcp.tool()
    def set_mod1_source_cc(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 SOURCE using CC method (CC #71).
        Args:
            value (int): Value for MOD 1 SOURCE:
                0 = TRIANGLE LFO
                21 = SQUARE LFO
                43 = SAW LFO
                64 = RAMP LFO
                85 = S&H LFO
                107 = F.EG/PGM
            channel (int): MIDI channel (default is 3).
        """
        midi.send_cc(channel, 71, value)

    @mcp.tool()
    def set_mod2_source(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 SOURCE (NRPN 465, MSB 3, LSB 81).
        Args:
            value (int): Value for MOD 2 SOURCE (0-6):
                0 = TRIANGLE LFO
                1 = SQUARE LFO
                2 = SAW LFO
                3 = RAMP LFO
                4 = S&H LFO
                5 = F.EG/PGM
                6 = Reserved
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 81, value)

    @mcp.tool()
    def set_mod2_source_cc(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 SOURCE using CC method (CC #72).
        Args:
            value (int): Value for MOD 2 SOURCE:
                0 = TRIANGLE LFO
                21 = SQUARE LFO
                43 = SAW LFO
                64 = RAMP LFO
                85 = S&H LFO
                107 = F.EG/PGM
            channel (int): MIDI channel (default is 3).
        """
        midi.send_cc(channel, 72, value)

    @mcp.tool()
    def set_mod1_osc_1_2_sel(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 OSC 1/2 SEL (CC #70).
        Args:
            value (int): Value for MOD 1 OSC 1/2 SEL:
                0 = OSC1 + OSC2
                43 = OSC1
                85 = OSC2
            channel (int): MIDI channel (default is 3).
        """
        midi.send_cc(channel, 70, value)

    @mcp.tool()
    def set_mod2_mwhl_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 MWHL AMT (NRPN 460, MSB 3, LSB 76).
        Args:
            value (int): Value for MOD 2 MWHL AMT (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 76, value)

    @mcp.tool()
    def set_mod2_velocity_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 VELOCITY AMT (NRPN 461, MSB 3, LSB 77).
        Args:
            value (int): Value for MOD 2 VELOCITY AMT (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 77, value)

    @mcp.tool()
    def set_mod2_pressure_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 PRESSURE AMT (NRPN 462, MSB 3, LSB 78).
        Args:
            value (int): Value for MOD 2 PRESSURE AMT (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 78, value)

    @mcp.tool()
    def set_mod2_ctl4_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 CTL4 AMT (NRPN 463, MSB 3, LSB 79).
        Args:
            value (int): Value for MOD 2 CTL4 AMT (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 79, value)

    @mcp.tool()
    def set_mod2_pgm_src(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 PGM SRC (NRPN 466, MSB 3, LSB 82).
        Args:
            value (int): Value for MOD 2 PGM SRC (0-8).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 82, value)

    @mcp.tool()
    def set_mod2_dest(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 DEST (NRPN 467, MSB 3, LSB 83).
        Args:
            value (int): Value for MOD 2 DEST (0-7):
                0 = LF01 Rate
                1 = VCA Level
                2 = OSC1 Wave
                3 = OSC1 + OSC2 Wave
                4 = OSC2 Wave
                5 = Noise Level
                6 = EG Time/PGM
                7 = Reserved
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 83, value)

    @mcp.tool()
    def set_mod2_pgm_dest(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 PGM DEST (NRPN 468, MSB 3, LSB 84).
        Args:
            value (int): Value for MOD 2 PGM DEST (0-89).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 84, value)

    @mcp.tool()
    def set_mod2_pgm_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 PGM AMT (NRPN 469, MSB 3, LSB 85).
        Args:
            value (int): Value for MOD 2 PGM AMT (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 85, value)

    @mcp.tool()
    def set_mod2_pitch_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 Pitch Amount (NRPN 470, MSB 3, LSB 86).
        Args:
            value (int): Value for MOD 2 Pitch Amount (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 86, value)

    @mcp.tool()
    def set_mod2_pitch_amt_normal(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 Pitch Amount using normal resolution (CC #15).
        Args:
            value (int): Value for MOD 2 Pitch Amount (0-127).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_cc(channel, 15, value)

    @mcp.tool()
    def set_mod2_filter_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 Filter Amount (NRPN 471, MSB 3, LSB 87).
        Args:
            value (int): Value for MOD 2 Filter Amount (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 87, value)

    @mcp.tool()
    def set_mod2_filter_amt_normal(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 Filter Amount using normal resolution (CC #16).
        Args:
            value (int): Value for MOD 2 Filter Amount (0-127).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_cc(channel, 16, value)

    @mcp.tool()
    def set_mod2_pitch_dest(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 PITCH DEST (NRPN 472, MSB 3, LSB 88).
        Args:
            value (int): Value for MOD 2 PITCH DEST (0-3).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 88, value)

    @mcp.tool()
    def set_mod2_pgm_dest_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 PGM Dest Amount using high-res CC (CC #17 [MSB], CC #49 [LSB]).
        Args:
            value (int): Value for MOD 2 PGM Dest Amount (0-127 for normal resolution, 0-16383 for high resolution).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_high_res_cc(channel, 17, 49, value)

    @mcp.tool()
    def set_mod2_pgm_dest_amt_normal(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 PGM Dest Amount using normal resolution (CC #17).
        Args:
            value (int): Value for MOD 2 PGM Dest Amount (0-127).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_cc(channel, 17, value)
