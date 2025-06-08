"""
Oscillator and Mod 2 tools for controlling oscillator and Mod 2 parameters on the Moog Sub 37.
"""

from mcp.server.fastmcp import FastMCP

from moog_sub37_mcp.midi.midi_manager import MIDIManager


def register_osc_tools(mcp: FastMCP, midi: MIDIManager):  # noqa: C901
    """
    Register all oscillator and Mod 2 tools with the MCP server.

    Args:
        mcp: The MCP server instance
        midi: The MIDI interface
    """

    @mcp.tool()
    def set_osc1_wave(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 1 Wave with high resolution.

        Args:
            value (int): High-resolution value for OSC 1 Wave (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 9, 41, value)

    @mcp.tool()
    def set_osc2_freq(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 2 Frequency with high resolution.

        Args:
            value (int): High-resolution value for OSC 2 Frequency (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 12, 44, value)

    @mcp.tool()
    def set_osc2_beat_freq(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 2 Beat Frequency with high resolution.

        Args:
            value (int): High-resolution value for OSC 2 Beat Frequency (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 13, 45, value)

    @mcp.tool()
    def set_osc2_wave(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 2 Wave with high resolution.

        Args:
            value (int): High-resolution value for OSC 2 Wave (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 14, 46, value)

    @mcp.tool()
    def set_mod2_pitch_amt_cc(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 Pitch Amount using high-res CC method (CC #15 [MSB], CC #47 [LSB]).

        Args:
            value (int): High-resolution value for MOD 2 Pitch Amount (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 15, 47, value)

    @mcp.tool()
    def set_mod2_filter_amt_cc(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 Filter Amount using high-res CC method (CC #16 [MSB], CC #48 [LSB]).

        Args:
            value (int): High-resolution value for MOD 2 Filter Amount (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 16, 48, value)

    @mcp.tool()
    def set_mod2_pgm_dest_amt_cc(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 Programmable Destination Amount using high-res CC method (CC #17 [MSB], CC #49 [LSB]).

        Args:
            value (int): High-resolution value for MOD 2 Programmable Destination Amount (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 17, 49, value)

    @mcp.tool()
    def set_osc1_octave(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 1 OCTAVE (NRPN 479, MSB 3, LSB 95).
        Args:
            value (int): Value for OSC 1 OCTAVE (0-3).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 95, value)

    @mcp.tool()
    def set_osc2_octave(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 2 OCTAVE (NRPN 483, MSB 3, LSB 99).
        Args:
            value (int): Value for OSC 2 OCTAVE (0-3).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 99, value)

    @mcp.tool()
    def set_osc2_hard_sync(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 2 HARD SYNC (NRPN 481, MSB 3, LSB 97).
        Args:
            value (int): Value for OSC 2 HARD SYNC (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 97, value)

    @mcp.tool()
    def set_osc_kb_reset(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC KB RESET (NRPN 482, MSB 3, LSB 98).
        Args:
            value (int): Value for OSC KB RESET (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 98, value)

    @mcp.tool()
    def set_mod2_osc_1_2_sel(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 Oscillator 1/2 Selection.

        Args:
            value (int): Value for oscillator selection (0 = OSC1 + OSC2, 43 = OSC1, 85 = OSC2).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 88, value)

    @mcp.tool()
    def set_mod2_dest_cc(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 2 Destination selection using CC method (CC #92).

        Args:
            value (int): Value for destination selection (0 = LF01 Rate, 18 = VCA Level, 37 = OSC1 Wave, 55 = OSC1 + OSC2 Wave, 73 = OSC2 Wave, 91 = Noise Level, 110 = EG Time/PGM).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 92, value)

    @mcp.tool()
    def set_pitch_bend_up_amount(value: int, channel: int = 3):  # type: ignore
        """
        Set the Pitch Bend Up Amount.

        Args:
            value (int): Value for Pitch Bend Up Amount (0-24, in semitones).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 107, value)

    @mcp.tool()
    def set_pitch_bend_down_amount(value: int, channel: int = 3):  # type: ignore
        """
        Set the Pitch Bend Down Amount.

        Args:
            value (int): Value for Pitch Bend Down Amount (0-24, in semitones).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 108, value)

    @mcp.tool()
    def set_filter_slopes(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter Slopes (Poles).

        Args:
            value (int): Value for Filter Slopes (0 = -6dB, 32 = -12dB, 64 = -18dB, 96 = -24dB).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 109, value)

    @mcp.tool()
    def set_osc_duo_mode(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC Duo Mode On/Off.

        Args:
            value (int): Value for OSC Duo Mode (0 = OFF, 64 = ON).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 110, value)

    @mcp.tool()
    def set_kb_ctrl_lo_hi(value: int, channel: int = 3):  # type: ignore
        """
        Set the Keyboard Control LO/HI.

        Args:
            value (int): Value for Keyboard Control (0 = NEITHER, 32 = LO, 64 = HI).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 111, value)

    @mcp.tool()
    def set_osc1_level(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 1 LEVEL (NRPN 489, MSB 3, LSB 105).
        Args:
            value (int): Value for OSC 1 LEVEL (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 105, value)

    @mcp.tool()
    def set_osc1_sub_level(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 1 Sub Level.

        Args:
            value (int): Value for OSC 1 Sub Level (0-127).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 115, value)

    @mcp.tool()
    def set_osc2_level(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 2 LEVEL (NRPN 493, MSB 3, LSB 109).
        Args:
            value (int): Value for OSC 2 LEVEL (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 109, value)

    @mcp.tool()
    def set_noise_level(value: int, channel: int = 3):  # type: ignore
        """
        Set the NOISE LEVEL (NRPN 496, MSB 3, LSB 112).
        Args:
            value (int): Value for NOISE LEVEL (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 112, value)

    @mcp.tool()
    def set_feedback_ext_level(value: int, channel: int = 3):  # type: ignore
        """
        Set the FB EXT LEVEL (NRPN 497, MSB 3, LSB 113).
        Args:
            value (int): Value for FB EXT LEVEL (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 113, value)

    @mcp.tool()
    def set_osc2_kb_ctrl(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 2 KB CTRL (NRPN 485, MSB 3, LSB 101).
        Args:
            value (int): Value for OSC 2 KB CTRL (0-2).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 101, value)

    @mcp.tool()
    def set_osc2_duo_mode(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 2 DUO MODE (NRPN 486, MSB 3, LSB 102).
        Args:
            value (int): Value for OSC 2 DUO MODE (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 102, value)

    @mcp.tool()
    def set_osc2_frequency(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 2 FREQUENCY (NRPN 487, MSB 3, LSB 103).
        Args:
            value (int): Value for OSC 2 FREQUENCY (0-2).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 103, value)

    @mcp.tool()
    def set_osc2_beat(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 2 BEAT (NRPN 488, MSB 3, LSB 104).
        Args:
            value (int): Value for OSC 2 BEAT (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 104, value)

    @mcp.tool()
    def set_osc1_on(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 1 ON (NRPN 490, MSB 3, LSB 106).
        Args:
            value (int): Value for OSC 1 ON (0-20).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 106, value)

    @mcp.tool()
    def set_sub_osc_on(value: int, channel: int = 3):  # type: ignore
        """
        Set the SUB OSC ON (NRPN 491, MSB 3, LSB 107).
        Args:
            value (int): Value for SUB OSC ON (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 107, value)

    @mcp.tool()
    def set_sub_osc_level(value: int, channel: int = 3):  # type: ignore
        """
        Set the SUB OSC LEVEL (NRPN 492, MSB 3, LSB 108).
        Args:
            value (int): Value for SUB OSC LEVEL (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 108, value)

    @mcp.tool()
    def set_osc2_on(value: int, channel: int = 3):  # type: ignore
        """
        Set the OSC 2 ON (NRPN 494, MSB 3, LSB 110).
        Args:
            value (int): Value for OSC 2 ON (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 110, value)

    @mcp.tool()
    def set_noise_on(value: int, channel: int = 3):  # type: ignore
        """
        Set the NOISE ON (NRPN 495, MSB 3, LSB 111).
        Args:
            value (int): Value for NOISE ON (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 111, value)

    @mcp.tool()
    def set_fb_ext_on(value: int, channel: int = 3):  # type: ignore
        """
        Set the FB EXT ON (NRPN 498, MSB 3, LSB 114).
        Args:
            value (int): Value for FB EXT ON (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 114, value)
