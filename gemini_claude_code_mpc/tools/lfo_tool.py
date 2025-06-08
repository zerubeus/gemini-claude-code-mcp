"""
LFO tools for controlling LFO parameters on the Digitone.
"""

from mcp.server.fastmcp import FastMCP

from moog_sub37_mcp.midi.midi_manager import MIDIManager


def register_lfo_tools(mcp: FastMCP, midi: MIDIManager):  # noqa: C901
    """
    Register all LFO tools with the MCP server.

    Args:
        mcp: The MCP server instance
        midi: The MIDI interface
    """

    @mcp.tool()
    def set_lfo1_rate(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 1 Rate (CC #3 [MSB], CC #35 [LSB]).
        Args:
            value (int): Value for LFO 1 Rate (0-127 for normal resolution, 0-16383 for high resolution).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_high_res_cc(channel, 3, 35, value)

    @mcp.tool()
    def set_lfo1_rate_normal(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 1 Rate using normal resolution (CC #3).
        Args:
            value (int): Value for LFO 1 Rate (0-127).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_lfo1_range(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 1 Range (NRPN 424, MSB 3, LSB 40).
        Args:
            value (int): Value for LFO 1 Range (0-2).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 40, value)

    @mcp.tool()
    def set_lfo1_sync(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 1 Sync (NRPN 425, MSB 3, LSB 41).
        Args:
            value (int): Value for LFO 1 Sync (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 41, value)

    @mcp.tool()
    def set_lfo1_kb_reset(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 1 KB Reset (NRPN 426, MSB 3, LSB 42).
        Args:
            value (int): Value for LFO 1 KB Reset (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 42, value)

    @mcp.tool()
    def set_lfo1_clk_div(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 1 Clock Divider (NRPN 427, MSB 3, LSB 43).
        Args:
            value (int): Value for LFO 1 Clock Divider (0-20).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 43, value)

    @mcp.tool()
    def set_lfo1_clk_src(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 1 Clock Source (NRPN 428, MSB 3, LSB 44).
        Args:
            value (int): Value for LFO 1 Clock Source (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 44, value)

    @mcp.tool()
    def set_lfo1_kb_track(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 1 KB Track (NRPN 430, MSB 3, LSB 46).
        Args:
            value (int): Value for LFO 1 KB Track (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 46, value)

    @mcp.tool()
    def set_lfo2_rate(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 Rate (NRPN 448, MSB 3, LSB 64).
        Args:
            value (int): Value for LFO 2 Rate (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 64, value)

    @mcp.tool()
    def set_lfo2_rate_normal(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 Rate using normal resolution (CC #8).
        Args:
            value (int): Value for LFO 2 Rate (0-127).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_range(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 Range (NRPN 449, MSB 3, LSB 65).
        Args:
            value (int): Value for LFO 2 Range (0-2).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 65, value)

    @mcp.tool()
    def set_lfo2_sync(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 Sync (NRPN 450, MSB 3, LSB 66).
        Args:
            value (int): Value for LFO 2 Sync (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 66, value)

    @mcp.tool()
    def set_lfo2_kb_reset(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 KB Reset (NRPN 451, MSB 3, LSB 67).
        Args:
            value (int): Value for LFO 2 KB Reset (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 67, value)

    @mcp.tool()
    def set_lfo2_clk_div(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 Clock Divider (NRPN 452, MSB 3, LSB 68).
        Args:
            value (int): Value for LFO 2 Clock Divider (0-20).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 68, value)

    @mcp.tool()
    def set_lfo2_clk_src(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 Clock Source (NRPN 453, MSB 3, LSB 69).
        Args:
            value (int): Value for LFO 2 Clock Source (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 69, value)

    @mcp.tool()
    def set_lfo2_kb_track(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 KB Track (NRPN 455, MSB 3, LSB 71).
        Args:
            value (int): Value for LFO 2 KB Track (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 71, value)

    @mcp.tool()
    def set_clock_divider_4_whole_notes(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for 4 whole notes.

        Args:
            value (int): The clock divider value (0-6, default 6).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_3_whole_notes(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for 3 whole notes.

        Args:
            value (int): The clock divider value (7-12, default 10).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_2_whole_notes(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for 2 whole notes.

        Args:
            value (int): The clock divider value (13-18, default 16).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_whole_note_half(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for whole note and a half.

        Args:
            value (int): The clock divider value (19-24, default 22).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_whole_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for whole note.

        Args:
            value (int): The clock divider value (25-40, default 32).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_dotted_half_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for dotted half note.

        Args:
            value (int): The clock divider value (31-36, default 34).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_whole_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for whole note triplet.

        Args:
            value (int): The clock divider value (37-42, default 40).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_half_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for half note.

        Args:
            value (int): The clock divider value (43-48, default 46).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_dotted_quarter_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for dotted quarter note triplet.

        Args:
            value (int): The clock divider value (49-54, default 52).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_half_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for half note triplet.

        Args:
            value (int): The clock divider value (55-60, default 58).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_quarter_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for quarter note.

        Args:
            value (int): The clock divider value (61-67, default 64).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_dotted_eighth_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for dotted eighth note.

        Args:
            value (int): The clock divider value (68-73, default 70).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_quarter_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for quarter note triplet.

        Args:
            value (int): The clock divider value (74-79, default 76).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_eighth_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for eighth note.

        Args:
            value (int): The clock divider value (80-85, default 82).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_dotted_sixteenth_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for dotted sixteenth note.

        Args:
            value (int): The clock divider value (86-91, default 88).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_eighth_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for eighth note triplet.

        Args:
            value (int): The clock divider value (92-97, default 94).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_sixteenth_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for sixteenth note.

        Args:
            value (int): The clock divider value (98-103, default 100).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_sixteenth_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for sixteenth note triplet.

        Args:
            value (int): The clock divider value (104-109, default 106).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_thirtysecond_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for thirty-second note.

        Args:
            value (int): The clock divider value (110-115, default 112).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_thirtysecond_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for thirty-second note triplet.

        Args:
            value (int): The clock divider value (116-121, default 118).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_clock_divider_sixtyfourth_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the clock divider for sixty-fourth note triplet.

        Args:
            value (int): The clock divider value (122-127, default 124).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 3, value)

    @mcp.tool()
    def set_lfo_rate(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO rate with high resolution.

        Args:
            value (int): High-resolution value for LFO rate (0-16383, default 9984).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 3, 34, value)

    @mcp.tool()
    def set_mod1_pitch_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 Pitch Amount (NRPN 445, MSB 3, LSB 61).
        Args:
            value (int): Value for MOD 1 Pitch Amount (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 61, value)

    @mcp.tool()
    def set_mod1_pitch_amt_normal(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 Pitch Amount using normal resolution (CC #4).
        Args:
            value (int): Value for MOD 1 Pitch Amount (0-127).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_cc(channel, 4, value)

    @mcp.tool()
    def set_mod1_filter_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 Filter Amount (NRPN 446, MSB 3, LSB 62).
        Args:
            value (int): Value for MOD 1 Filter Amount (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 62, value)

    @mcp.tool()
    def set_mod1_filter_amt_normal(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 Filter Amount using normal resolution (CC #11).
        Args:
            value (int): Value for MOD 1 Filter Amount (0-127).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_cc(channel, 11, value)

    @mcp.tool()
    def set_mod1_pgm_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 PGM Amount (NRPN 444, MSB 3, LSB 60).
        Args:
            value (int): Value for MOD 1 PGM Amount (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 60, value)

    @mcp.tool()
    def set_mod1_pgm_dest_amt_normal(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 PGM Dest Amount using normal resolution (CC #20).
        Args:
            value (int): Value for MOD 1 PGM Dest Amount (0-127).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_cc(channel, 20, value)

    @mcp.tool()
    def set_mod1_pgm_src(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 PGM SRC (NRPN 441, MSB 3, LSB 57).
        Args:
            value (int): Value for MOD 1 PGM SRC (0-8).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 57, value)

    @mcp.tool()
    def set_mod1_dest(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 DEST (NRPN 442, MSB 3, LSB 58).
        Args:
            value (int): Value for MOD 1 DEST (0-7):
                0 = LF02 Rate
                1 = VCA Level
                2 = OSC1 Wave
                3 = OSC1 + OSC2 Wave
                4 = OSC2 Wave
                5 = Noise Level
                6 = EG Time/PGM
                7 = Reserved
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 58, value)

    @mcp.tool()
    def set_mod1_pgm_dest(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 PGM DEST (NRPN 443, MSB 3, LSB 59).
        Args:
            value (int): Value for MOD 1 PGM DEST (0-89).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 59, value)

    @mcp.tool()
    def set_mod1_pitch_dest(value: int, channel: int = 3):  # type: ignore
        """
        Set the MOD 1 PITCH DEST (NRPN 447, MSB 3, LSB 63).
        Args:
            value (int): Value for MOD 1 PITCH DEST (0-3).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 63, value)

    @mcp.tool()
    def set_lfo2_clock_divider_4_whole_notes(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for 4 whole notes.

        Args:
            value (int): The clock divider value (0-6, default 6).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_3_whole_notes(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for 3 whole notes.

        Args:
            value (int): The clock divider value (7-12, default 10).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_2_whole_notes(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for 2 whole notes.

        Args:
            value (int): The clock divider value (13-18, default 16).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_whole_note_half(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for whole note and a half.

        Args:
            value (int): The clock divider value (19-24, default 22).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_whole_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for whole note.

        Args:
            value (int): The clock divider value (25-40, default 32).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_dotted_half_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for dotted half note.

        Args:
            value (int): The clock divider value (31-36, default 34).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_whole_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for whole note triplet.

        Args:
            value (int): The clock divider value (37-42, default 40).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_half_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for half note.

        Args:
            value (int): The clock divider value (43-48, default 46).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_dotted_quarter_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for dotted quarter note triplet.

        Args:
            value (int): The clock divider value (49-54, default 52).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_half_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for half note triplet.

        Args:
            value (int): The clock divider value (55-60, default 58).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_quarter_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for quarter note.

        Args:
            value (int): The clock divider value (61-67, default 64).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_dotted_eighth_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for dotted eighth note.

        Args:
            value (int): The clock divider value (68-73, default 70).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_quarter_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for quarter note triplet.

        Args:
            value (int): The clock divider value (74-79, default 76).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_eighth_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for eighth note.

        Args:
            value (int): The clock divider value (80-85, default 82).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_dotted_sixteenth_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for dotted sixteenth note.

        Args:
            value (int): The clock divider value (86-91, default 88).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_eighth_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for eighth note triplet.

        Args:
            value (int): The clock divider value (92-97, default 94).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_sixteenth_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for sixteenth note.

        Args:
            value (int): The clock divider value (98-103, default 100).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_sixteenth_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for sixteenth note triplet.

        Args:
            value (int): The clock divider value (104-109, default 106).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_thirtysecond_note(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for thirty-second note.

        Args:
            value (int): The clock divider value (110-115, default 112).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_thirtysecond_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for thirty-second note triplet.

        Args:
            value (int): The clock divider value (116-121, default 118).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_clock_divider_sixtyfourth_note_triplet(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 clock divider for sixty-fourth note triplet.

        Args:
            value (int): The clock divider value (122-127, default 124).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 8, value)

    @mcp.tool()
    def set_lfo2_kb_reset_cc(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 Keyboard Reset using CC method.

        Args:
            value (int): Value for keyboard reset (0 = OFF, 64 = ON).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 95, value)

    @mcp.tool()
    def set_lfo2_range_cc(value: int, channel: int = 3):  # type: ignore
        """
        Set the LFO 2 Range selection using CC method.

        Args:
            value (int): Value for range selection (0 = Low Range, 43 = Med Range, 85 = Hi Range).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 78, value)
