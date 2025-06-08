# Moog Sub37 MCP

A Model Context Protocol (MCP) server that allows Claude and other MCP-compatible LLMs to interact with and control the Moog Sub37/Subsequent37 analog synthesizer via MIDI. This integration enables AI-assisted sound design and parameter control of this legendary Moog synthesizer.

## About the Moog Sub37/Subsequent37

The Moog Sub37/Subsequent37 is a powerful analog synthesizer featuring:

- 2 oscillators with sub oscillators
- Classic Moog ladder filter
- Dual LFOs
- Extensive modulation options
- 256 preset memory
- 37-key keyboard with velocity and aftertouch
- Mono and Duo (paraphonic) modes
- Built-in arpeggiator and step sequencer

# Prompt Examples

Prompt should start with "use Moog sub37 MCP to ..."

```
"Design a deep, resonant bass patch using the Moog filter's self-oscillation on midi channel 3"
"Create an evolving pad sound using both oscillators in Duo mode on midi channel 3"
"Program a sequence that showcases the Sub37's classic Moog lead sound on midi channel 3"
"Design a dark atmospheric sound using the Sub37's modulation capabilities on midi channel 3"
"Create a punchy bass sound perfect for techno using the multidrive circuit on midi channel 3"
```

## Features

- [x] Complete MIDI control interface for all Sub37/Subsequent37 parameters
- [x] Support for both Sub37 and Subsequent37 models
- [x] Access to all synthesis parameters:
  - Oscillator controls (waveform, pitch, sync)
  - Filter controls (cutoff, resonance, envelope amount)
  - Envelope generators
  - LFO settings
  - Modulation routing
  - Arpeggiator/Sequencer parameters
- [x] Preset management
- [x] Real-time parameter automation

## Demo

Watch Claude control the Moog Sub37/Subsequent37 in real-time:

coming soon

## Installation and Usage

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) for package management
- A Moog Sub37 or Subsequent37 synthesizer connected via USB
- Claude Desktop app (for full integration)

### Installing Dependencies

uv is mandatory for this project. Start by installing it:

#### For macOS:

```bash
brew install uv
```

#### For Windows:

Follow the instructions [here](https://docs.astral.sh/uv/getting-started/installation/)

### Installing with Claude Desktop

To use with Claude AI, add the MCP server configuration in Claude Desktop:

⚠️ **Important**: You don't need to clone the repository or install the packages manually. The MCP server is published on PyPI and can be installed automatically.

Go to Claude > Settings > Developer > Edit Config > claude_desktop_config.json to include the following:

```json
{
  "mcpServers": {
    "Sub37": {
      "command": "uvx",
      "args": ["moog-sub37-mcp"]
    }
  }
}
```

## Implementation Details

This library leverages:

- **FastMCP**: For exposing synth controls to LLMs
- **mido**: For reliable MIDI communication with the synthesizer

## Use Cases

- **AI-Assisted Sound Design**: Let Claude help you create new sounds and explore the synth's capabilities

## Community and Support

- Join our [Discord community](https://discord.gg/ZFuSuegBMS) for help and discussion
- Visit [synthgenie.com](https://www.synthgenie.com/) for the web-based version (API key available for free on Discord)
- Report issues and contribute on GitHub

## License

MIT License - See LICENSE file for details
