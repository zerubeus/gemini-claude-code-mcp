"""
Filter tools for controlling filter and filter envelope parameters on the Moog Sub 37.
"""

from mcp.server.fastmcp import FastMCP

from moog_sub37_mcp.midi.midi_manager import MIDIManager


def register_filter_tools(mcp: FastMCP, midi: MIDIManager):
    """
    Register all filter and filter envelope tools with the MCP server.

    Args:
        mcp: The MCP server instance
        midi: The MIDI interface
    """

    @mcp.tool()
    def set_filter_multidrive(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter Multidrive with high resolution.

        Args:
            value (int): High-resolution value for Filter Multidrive (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 18, 50, value)

    @mcp.tool()
    def set_filter_cutoff(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter Cutoff with high resolution.

        Args:
            value (int): High-resolution value for Filter Cutoff (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 19, 51, value)

    @mcp.tool()
    def set_filter_resonance(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter Resonance with high resolution.

        Args:
            value (int): High-resolution value for Filter Resonance (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 21, 53, value)

    @mcp.tool()
    def set_filter_kb_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter Keyboard Amount with high resolution.

        Args:
            value (int): High-resolution value for Filter Keyboard Amount (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 22, 54, value)

    @mcp.tool()
    def set_filter_eg_attack_time(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter EG Attack Time with high resolution.

        Args:
            value (int): High-resolution value for Filter EG Attack Time (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 23, 55, value)

    @mcp.tool()
    def set_filter_eg_decay_time(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter EG Decay Time with high resolution.

        Args:
            value (int): High-resolution value for Filter EG Decay Time (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 24, 56, value)

    @mcp.tool()
    def set_filter_eg_sustain_time(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter EG Sustain Time with high resolution.

        Args:
            value (int): High-resolution value for Filter EG Sustain Time (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 25, 57, value)

    @mcp.tool()
    def set_filter_eg_release_time(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter EG Release Time with high resolution.

        Args:
            value (int): High-resolution value for Filter EG Release Time (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 26, 58, value)

    @mcp.tool()
    def set_filter_eg_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter EG Amount with high resolution.

        Args:
            value (int): High-resolution value for Filter EG Amount (0-16383).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_high_res_cc(channel, 27, 59, value)

    @mcp.tool()
    def set_filter_eg_kb_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter EG Keyboard Amount.

        Args:
            value (int): Value for Filter EG Keyboard Amount (0-127).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 79, value)

    @mcp.tool()
    def set_amp_eg_kb_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the AMP EG Keyboard Amount.

        Args:
            value (int): Value for AMP EG Keyboard Amount (0-127).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 80, value)

    @mcp.tool()
    def set_filter_eg_reset(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter EG Reset.

        Args:
            value (int): Value for Filter EG Reset (0 = OFF, 64 = ON).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 82, value)

    @mcp.tool()
    def set_amp_eg_reset(value: int, channel: int = 3):  # type: ignore
        """
        Set the AMP EG Reset.

        Args:
            value (int): Value for AMP EG Reset (0 = OFF, 64 = ON).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 83, value)

    @mcp.tool()
    def set_filter_eg_vel_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter EG Velocity Amount.

        Args:
            value (int): Value for Filter EG Velocity Amount (0-127).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 86, value)

    @mcp.tool()
    def set_amp_eg_vel_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the AMP EG Velocity Amount.

        Args:
            value (int): Value for AMP EG Velocity Amount (0-127).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 87, value)

    @mcp.tool()
    def set_filter_eg_delay(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter EG Delay.

        Args:
            value (int): Value for Filter EG Delay (0-127).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 103, value)

    @mcp.tool()
    def set_amp_eg_delay(value: int, channel: int = 3):  # type: ignore
        """
        Set the AMP EG Delay.

        Args:
            value (int): Value for AMP EG Delay (0-127).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 104, value)

    @mcp.tool()
    def set_filter_eg_hold(value: int, channel: int = 3):  # type: ignore
        """
        Set the Filter EG Hold.

        Args:
            value (int): Value for Filter EG Hold (0-127).
            channel (int): MIDI channel (default is 3 if not specified).
        """
        midi.send_cc(channel, 105, value)

    @mcp.tool()
    def set_filter_cutoff_alt(value: int, channel: int = 3):  # type: ignore
        """
        Set the FILTER CUTOFF (NRPN 499, MSB 3, LSB 115).
        Args:
            value (int): Value for FILTER CUTOFF (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 115, value)

    @mcp.tool()
    def set_filter_resonance_alt(value: int, channel: int = 3):  # type: ignore
        """
        Set the FILTER RESONANCE (NRPN 500, MSB 3, LSB 116).
        Args:
            value (int): Value for FILTER RESONANCE (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 116, value)

    @mcp.tool()
    def set_filter_drive(value: int, channel: int = 3):  # type: ignore
        """
        Set the FILTER DRIVE (NRPN 501, MSB 3, LSB 117).
        Args:
            value (int): Value for FILTER DRIVE (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 117, value)

    @mcp.tool()
    def set_filter_slope(value: int, channel: int = 3):  # type: ignore
        """
        Set the FILTER SLOPE (NRPN 502, MSB 3, LSB 118).
        Args:
            value (int): Value for FILTER SLOPE (0-3).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 118, value)

    @mcp.tool()
    def set_filter_eg_amt_alt(value: int, channel: int = 3):  # type: ignore
        """
        Set the FILTER EG AMT (NRPN 503, MSB 3, LSB 119).
        Args:
            value (int): Value for FILTER EG AMT (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 119, value)

    @mcp.tool()
    def set_filter_kb_amt_alt(value: int, channel: int = 3):  # type: ignore
        """
        Set the FILTER KB AMT (NRPN 504, MSB 3, LSB 120).
        Args:
            value (int): Value for FILTER KB AMT (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 120, value)

    @mcp.tool()
    def set_f_eg_attack(value: int, channel: int = 3):  # type: ignore
        """
        Set the F EG ATTACK (NRPN 505, MSB 3, LSB 121).
        Args:
            value (int): Value for F EG ATTACK (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 121, value)

    @mcp.tool()
    def set_f_eg_decay(value: int, channel: int = 3):  # type: ignore
        """
        Set the F EG DECAY (NRPN 506, MSB 3, LSB 122).
        Args:
            value (int): Value for F EG DECAY (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 122, value)

    @mcp.tool()
    def set_f_eg_sustain(value: int, channel: int = 3):  # type: ignore
        """
        Set the F EG SUSTAIN (NRPN 507, MSB 3, LSB 123).
        Args:
            value (int): Value for F EG SUSTAIN (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 123, value)

    @mcp.tool()
    def set_f_eg_release(value: int, channel: int = 3):  # type: ignore
        """
        Set the F EG RELEASE (NRPN 508, MSB 3, LSB 124).
        Args:
            value (int): Value for F EG RELEASE (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 124, value)

    @mcp.tool()
    def set_f_eg_delay(value: int, channel: int = 3):  # type: ignore
        """
        Set the F EG DELAY (NRPN 509, MSB 3, LSB 125).
        Args:
            value (int): Value for F EG DELAY (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 125, value)

    @mcp.tool()
    def set_f_eg_hold(value: int, channel: int = 3):  # type: ignore
        """
        Set the F EG HOLD (NRPN 510, MSB 3, LSB 126).
        Args:
            value (int): Value for F EG HOLD (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 126, value)

    @mcp.tool()
    def set_f_eg_vel_amt(value: int, channel: int = 3):  # type: ignore
        """
        Set the F EG VEL AMT (NRPN 511, MSB 3, LSB 127).
        Args:
            value (int): Value for F EG VEL AMT (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 3, 127, value)

    @mcp.tool()
    def set_f_eg_kb_track(value: int, channel: int = 3):  # type: ignore
        """
        Set the F EG KB TRACK (NRPN 512, MSB 4, LSB 0).
        Args:
            value (int): Value for F EG KB TRACK (0-16383).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 4, 0, value)

    @mcp.tool()
    def set_f_eg_multi_trig(value: int, channel: int = 3):  # type: ignore
        """
        Set the F EG MULTI TRIG (NRPN 513, MSB 4, LSB 1).
        Args:
            value (int): Value for F EG MULTI TRIG (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 4, 1, value)

    @mcp.tool()
    def set_f_eg_reset(value: int, channel: int = 3):  # type: ignore
        """
        Set the F EG RESET (NRPN 514, MSB 4, LSB 2).
        Args:
            value (int): Value for F EG RESET (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 4, 2, value)

    @mcp.tool()
    def set_f_eg_sync(value: int, channel: int = 3):  # type: ignore
        """
        Set the F EG SYNC (NRPN 515, MSB 4, LSB 3).
        Args:
            value (int): Value for F EG SYNC (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 4, 3, value)

    @mcp.tool()
    def set_f_eg_loop(value: int, channel: int = 3):  # type: ignore
        """
        Set the F EG LOOP (NRPN 516, MSB 4, LSB 4).
        Args:
            value (int): Value for F EG LOOP (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 4, 4, value)

    @mcp.tool()
    def set_f_eg_latch(value: int, channel: int = 3):  # type: ignore
        """
        Set the F EG LATCH (NRPN 517, MSB 4, LSB 5).
        Args:
            value (int): Value for F EG LATCH (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 4, 5, value)

    @mcp.tool()
    def set_f_eg_clk_div(value: int, channel: int = 3):  # type: ignore
        """
        Set the F EG CLK DIV (NRPN 518, MSB 4, LSB 6).
        Args:
            value (int): Value for F EG CLK DIV (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 4, 6, value)

    @mcp.tool()
    def set_f_eg_attk_exp(value: int, channel: int = 3):  # type: ignore
        """
        Set the F EG ATTK EXP (NRPN 520, MSB 4, LSB 8).
        Args:
            value (int): Value for F EG ATTK EXP (0-1).
            channel (int): MIDI channel (default is 3).
        """
        midi.send_nrpn(channel, 4, 8, value)
