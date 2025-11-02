# VRChat AI Bot - TTS/STT System

A sophisticated AI companion bot for VRChat that provides real-time speech-to-text and text-to-speech capabilities with intelligent conversation management and memory systems.

## 🚀 Overview

This project creates an AI companion that can engage in natural conversations within VRChat environments. The system combines real-time speech processing with large language models to create an immersive, interactive experience.

### Key Features

- **Real-time Speech-to-Text**: Continuous audio transcription using RealtimeSTT
- **High-Quality Text-to-Speech**: Natural voice synthesis with Piper TTS
- **Intelligent Conversation**: Context-aware responses using LLMs via OpenRouter
- **Memory Systems**: Both short-term conversation memory and long-term vector storage
- **VRChat Integration**: Designed specifically for virtual reality social interactions
- **Modular Architecture**: Clean separation of concerns with planned enhancements

## 🏗️ Architecture

The system follows a modular architecture with clear separation between input processing, intelligence layer, and output generation:

```
Input Layer → Processing Layer → Output Layer
    ↓              ↓               ↓
Speech-to-Text → LLM Interface → Text-to-Speech
OSC Events    → Prompt Generator → OSC Commands
Computer Vision → State Manager → VRChat API
```

### Core Components

- **Main Application** ([`Core/Main.py`](Core/Main.py:1)): Orchestrates the conversation flow
- **Speech Processing** ([`Core/Speech_To_Text.py`](Core/Speech_To_Text.py:1), [`Core/Text_To_Speech.py`](Core/Text_To_Speech.py:1)): Handles audio input/output
- **Memory Management** ([`Core/Chat_Memory.py`](Core/Chat_Memory.py:1)): Short-term and long-term memory systems
- **LLM Integration** ([`Core/callLLM.py`](Core/callLLM.py:1)): Communication with language models
- **Configuration** ([`Core/Config_Manager.py`](Core/Config_Manager.py:1)): Centralized settings management

## 🛠️ Installation

### Prerequisites

- Python 3.9+
- Audio input/output devices
- OpenRouter API key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "tts stt ai"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```

4. **Configure audio devices**
   Edit [`Core/config/config.yaml`](Core/config/config.yaml:1) to set your audio input/output device indices:
   ```yaml
   audio:
     input_device: 6    # Your microphone device index
     output_device: 11  # Your speaker/headphone device index
     volume: 1
     length_scale: 1
     noise_scale: 0
     noise_w_scale: 0
     normalize_audio: false
   ```

5. **Download TTS model**
   Place the Piper TTS model file (`glados_piper_medium.onnx`) in the `Models/` directory.

## 🎮 Usage

### Basic Operation

1. **Start the application**:
   ```bash
   python Core/Main.py
   ```

2. **Choose input method**:
   - Type 'yes' for text-based input
   - Press Enter for speech input (wait for "speak now" prompt)

3. **Interact naturally**:
   - Speak or type your messages
   - The AI will respond with synthesized speech
   - Type "exit chat" to end the conversation

### Advanced Features

- **Memory System**: The bot maintains conversation context and stores important memories in a vector database
- **Custom Personalities**: Modify [`Core/config/vrchat_bot_prompt.md`](Core/config/vrchat_bot_prompt.md:1) to change the AI's personality and behavior
- **Audio Configuration**: Adjust TTS parameters in the config file for different voice characteristics

## 📁 Project Structure

```
tts stt ai/
├── Core/
│   ├── Main.py                 # Main application orchestrator
│   ├── Speech_To_Text.py       # Real-time speech transcription
│   ├── Text_To_Speech.py       # Voice synthesis with Piper TTS
│   ├── Chat_Memory.py          # Short-term and vector memory systems
│   ├── callLLM.py              # LLM integration via OpenRouter
│   ├── Config_Manager.py       # Configuration management
│   ├── Convo_Manager.py        # Conversation state tracking
│   └── config/
│       ├── config.yaml         # Audio and system settings
│       └── vrchat_bot_prompt.md # AI personality and behavior
├── Plans/                      # Architecture and roadmap documentation
├── Models/                     # TTS model files (glados_piper_medium.onnx)
├── Test/                       # Testing and experimentation scripts
└── README.md                   # This file
```

## 🔧 Configuration

### Audio Settings

Configure audio devices in [`Core/config/config.yaml`](Core/config/config.yaml:1):

```yaml
audio:
  input_device: 6      # Microphone device index
  output_device: 11    # Speaker device index  
  volume: 1            # TTS volume (0.0 - 1.0)
  length_scale: 1      # Speech speed (lower = faster)
  noise_scale: 0       # Voice variation
  noise_w_scale: 0     # Additional voice variation
  normalize_audio: false
```

### AI Personality

Customize the bot's behavior in [`Core/config/vrchat_bot_prompt.md`](Core/config/vrchat_bot_prompt.md:1):

- Modify the system prompt to change personality traits
- Adjust communication style and interaction guidelines
- Set VRChat-specific knowledge and social boundaries

## 🚀 Development Roadmap

### Current Implementation
- ✅ Real-time speech-to-text and text-to-speech
- ✅ Basic conversation flow with LLM integration  
- ✅ Short-term memory management
- ✅ Vector-based long-term memory storage
- ✅ Configurable audio settings

### Planned Enhancements
See [`Plans/implementation_roadmap.md`](Plans/implementation_roadmap.md:1) for detailed development timeline:

- **Phase 1**: Modular architecture and configuration system
- **Phase 2**: OSC communication for VRChat integration
- **Phase 3**: Advanced prompt generation and context awareness
- **Phase 4**: Computer vision and enhanced interactions
- **Phase 5**: Performance optimization and production readiness

## 🐛 Troubleshooting

### Common Issues

**Audio Device Problems**
- Check device indices in Windows Sound settings
- Verify `input_device` and `output_device` values in config.yaml
- Ensure microphone permissions are granted

**TTS Model Issues**
- Confirm `glados_piper_medium.onnx` is in the Models/ directory
- Check Piper voice model compatibility

**API Connection Problems**
- Verify OpenRouter API key in .env file
- Check internet connectivity
- Monitor API rate limits and quotas

**Memory System Errors**
- Ensure ChromaDB can create the `my_vectors` directory
- Check disk space for vector storage

## 🤝 Contributing

This project is actively developed with a modular architecture approach. Contributions are welcome in areas such as:

- Enhanced error handling and recovery
- Additional TTS voice models
- Improved memory management algorithms
- VRChat OSC integration features
- Performance optimizations

Please refer to the architecture plans in the `Plans/` directory for implementation guidelines.

## 📄 License

This project is for educational and development purposes. Please ensure compliance with the terms of service for all integrated services (OpenRouter, VRChat, etc.).

## 🙏 Acknowledgments

- **RealtimeSTT**: For real-time speech-to-text capabilities
- **Piper TTS**: For high-quality text-to-speech synthesis
- **OpenRouter**: For LLM API access
- **ChromaDB**: For vector memory storage
- **VRChat Community**: For inspiration and use cases

---

*For detailed technical specifications and development roadmap, see the documentation in the `Plans/` directory.*