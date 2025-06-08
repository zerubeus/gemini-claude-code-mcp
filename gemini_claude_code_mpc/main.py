import logging
import sys

from moog_sub37_mcp.mcp_server.server import mcp
from moog_sub37_mcp.midi.midi_manager import MIDIManager

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def check_midi_connection():
    """Verify MIDI connection before starting the server"""
    try:
        midi = MIDIManager(port_name='Moog Sub 37')
        if not midi.connected:
            logger.error('Could not connect to Moog Sub 37. Please check your USB connection.')
            logger.info(f'Available MIDI ports: {midi.list_ports()}')
            return False
        logger.info(f'Successfully connected to MIDI device: {midi.output_port}')
        return True
    except Exception as e:
        logger.error(f'ERROR connecting to MIDI: {str(e)}')
        return False


def main():
    """Entry point for the sub37-mcp command"""
    logger.info('Starting Moog Sub37 MCP server...')

    # Verify MIDI connection before starting server
    if not check_midi_connection():
        logger.warning('MIDI connection failed. Server will start but may not function correctly.')

    try:
        logger.info('Starting MCP server...')
        mcp.run()
    except Exception as e:
        logger.error(f'ERROR running MCP server: {str(e)}', exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
