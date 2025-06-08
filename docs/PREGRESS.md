This app is a Model Context Protocol server that allows Claude and other MCP-compatible LLMs to interact with Moog Sub37 via MIDI.

## Features

- [x] use uv for dependency/project management
- [x] use pydantic for config validation
- [x] use pytest for testing
- [x] map all moog sub37 config params to MIDI values and display values in `moog_sub37_mcp/moodsub37/moodsub37_config.py`
- [x] structure moog sub37 config into models, constants, and utils
- [x] add tests for all moog sub37 config params (amp, fx, lfo, filters..)
- [x] add a new utility in `moog_sub37_mcp/midi/` to handle MIDI communication with moog sub37, should include channel selection, CC messages, midi value, etc.
