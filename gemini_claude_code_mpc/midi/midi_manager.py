"""
MIDI Interface

This module handles MIDI communication.
It provides functionality for connecting to MIDI devices over USB,
selecting channels, and sending control change (CC) messages
"""

import logging
from typing import Optional

import mido

logger = logging.getLogger(__name__)


class MIDIManager:
    """Interface for MIDI communication."""

    def __init__(self, port_name: str):
        """
        Initialize the MIDI interface.

        Args:
            port_name: Name of the MIDI port to use.
        """
        self.input_port: Optional[mido.ports.BaseInput] = None
        self.output_port: Optional[mido.ports.BaseOutput] = None
        self.connected = False

        if port_name:
            self.connect(port_name)

    def list_ports(self) -> list[str]:
        """List available MIDI ports."""
        inputs = mido.get_input_names()  # type: ignore[attr-defined]
        outputs = mido.get_output_names()  # type: ignore[attr-defined]
        return list(set(inputs + outputs))  # type: ignore[arg-type]

    def connect(self, port_name: str) -> bool:
        """
        Connect to the specified MIDI port.

        Args:
            port_name: Name of the MIDI port to connect to

        Returns:
            bool: True if connection successful, False otherwise.
        """
        try:
            # Close existing connections if any
            self.disconnect()

            # Open new connections
            self.output_port = mido.open_output(port_name)  # type: ignore[attr-defined]
            try:
                self.input_port = mido.open_input(port_name)  # type: ignore[attr-defined]
            except (OSError, ValueError) as e:
                logger.warning(f'Could not open input port {port_name}: {e}')

            self.connected = True
            logger.info(f'Connected to MIDI port: {port_name}')
            return True
        except (OSError, ValueError) as e:
            logger.error(f'Failed to connect to MIDI port {port_name}: {e}')
            self.disconnect()
            return False

    def disconnect(self) -> None:
        """Close all MIDI connections."""
        if self.input_port:
            self.input_port.close()
            self.input_port = None

        if self.output_port:
            self.output_port.close()
            self.output_port = None

        self.connected = False

    def send_cc(self, channel: int, cc: int, value: int) -> bool:
        """
        Send a Control Change (CC) message.

        Args:
            channel: MIDI channel (1-16)
            cc: Control Change number (0-127)
            value: Control Change value (0-127)

        Returns:
            bool: True if message sent successfully, False otherwise.
        """
        if not self.connected or not self.output_port:
            logger.error('Not connected to any MIDI port')
            return False

        # Convert 1-indexed channel to 0-indexed
        if 1 <= channel <= 16:
            channel = channel - 1
        else:
            logger.error(f'Invalid channel: {channel}. Must be between 1-16.')
            return False

        try:
            # Create and send the CC message
            msg = mido.Message('control_change', channel=channel, control=cc, value=value)
            self.output_port.send(msg)  # type: ignore[attr-defined]
            logger.debug(f'Sent CC: channel={channel + 1}, cc={cc}, value={value}')
            return True
        except Exception as e:
            logger.error(f'Error sending CC message: {e}')
            return False

    def send_high_res_cc(self, channel: int, cc_msb: int, cc_lsb: int, value: int) -> bool:
        """
        Send a high-resolution Control Change (CC) message using MSB and LSB.

        Args:
            channel: MIDI channel (1-16)
            cc_msb: Control Change number for MSB (0-127)
            cc_lsb: Control Change number for LSB (0-127)
            value: High-resolution value (0-16383)

        Returns:
            bool: True if message sent successfully, False otherwise.
        """
        if not self.connected or not self.output_port:
            logger.error('Not connected to any MIDI port')
            return False

        # Convert 1-indexed channel to 0-indexed
        if 1 <= channel <= 16:
            channel = channel - 1
        else:
            logger.error(f'Invalid channel: {channel}. Must be between 1-16.')
            return False

        # Validate value range
        if not 0 <= value <= 16383:
            logger.error(f'Invalid high-res value: {value}. Must be between 0-16383.')
            return False

        try:
            # Split value into MSB and LSB
            msb = (value >> 7) & 0x7F  # Most significant 7 bits
            lsb = value & 0x7F  # Least significant 7 bits

            # First reset both controllers to 0 to ensure proper initialization
            msg_msb_reset = mido.Message('control_change', channel=channel, control=cc_msb, value=0)
            msg_lsb_reset = mido.Message('control_change', channel=channel, control=cc_lsb, value=0)

            # Then send the actual values - LSB must be sent before MSB for proper operation
            msg_lsb = mido.Message('control_change', channel=channel, control=cc_lsb, value=lsb)
            msg_msb = mido.Message('control_change', channel=channel, control=cc_msb, value=msb)

            # Send messages in the correct order with proper timing
            self.output_port.send(msg_msb_reset)  # type: ignore[attr-defined]
            self.output_port.send(msg_lsb_reset)  # type: ignore[attr-defined]
            self.output_port.send(msg_lsb)  # type: ignore[attr-defined]
            self.output_port.send(msg_msb)  # type: ignore[attr-defined]

            logger.debug(
                f'Sent high-res CC: channel={channel + 1}, cc_msb={cc_msb}, cc_lsb={cc_lsb}, value={value} (msb={msb}, lsb={lsb})'
            )
            return True
        except Exception as e:
            logger.error(f'Error sending high-res CC message: {e}')
            return False

    def send_nrpn(self, channel: int, nrpn_msb: int, nrpn_lsb: int, value: int) -> bool:
        """
        Send a Non-Registered Parameter Number (NRPN) message with high resolution value.

        Args:
            channel: MIDI channel (1-16)
            nrpn_msb: NRPN Most Significant Byte (CC 99 value, 0-127)
            nrpn_lsb: NRPN Least Significant Byte (CC 98 value, 0-127)
            value: High-resolution value for the parameter (0-16383)

        Returns:
            bool: True if message sent successfully, False otherwise.
        """
        if not self.connected or not self.output_port:
            logger.error('Not connected to any MIDI port')
            return False

        # Convert 1-indexed channel to 0-indexed
        if 1 <= channel <= 16:
            channel = channel - 1
        else:
            logger.error(f'Invalid channel: {channel}. Must be between 1-16.')
            return False

        # Validate value range
        if not 0 <= value <= 16383:
            logger.error(f'Invalid NRPN value: {value}. Must be between 0-16383.')
            return False

        try:
            # Split value into MSB and LSB
            value_msb = (value >> 7) & 0x7F  # Most significant 7 bits
            value_lsb = value & 0x7F  # Least significant 7 bits

            # Send NRPN messages in the correct order:
            # 1. NRPN MSB (CC 99)
            # 2. NRPN LSB (CC 98)
            # 3. Data Entry MSB (CC 6)
            # 4. Data Entry LSB (CC 38)
            msg_nrpn_msb = mido.Message('control_change', channel=channel, control=99, value=nrpn_msb)
            msg_nrpn_lsb = mido.Message('control_change', channel=channel, control=98, value=nrpn_lsb)
            msg_data_msb = mido.Message('control_change', channel=channel, control=6, value=value_msb)
            msg_data_lsb = mido.Message('control_change', channel=channel, control=38, value=value_lsb)

            self.output_port.send(msg_nrpn_msb)  # type: ignore[attr-defined]
            self.output_port.send(msg_nrpn_lsb)  # type: ignore[attr-defined]
            self.output_port.send(msg_data_msb)  # type: ignore[attr-defined]
            self.output_port.send(msg_data_lsb)  # type: ignore[attr-defined]

            logger.debug(f'Sent NRPN: channel={channel + 1}, nrpn_msb={nrpn_msb}, nrpn_lsb={nrpn_lsb}, value={value}')
            return True
        except Exception as e:
            logger.error(f'Error sending NRPN message: {e}')
            return False
