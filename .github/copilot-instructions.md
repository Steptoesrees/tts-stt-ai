# AI Coding Agent Instructions for TTS-STT-AI Project

## Project Overview
This is a real-time voice conversation system that implements GLaDOS from Portal games. The system combines speech-to-text, LLM processing, and text-to-speech to create an interactive voice assistant.

## Architecture & Core Components

### Main Application Flow (`Main.py`)
- **Entry point**: `Main.py` contains the main conversation loop
- **Audio cue system**: Plays 440Hz tone (0.3s) to signal user can speak
- **Message handling**: Maintains conversation history with role-based messages
- **Exit handling**: Special logic for "exit chat" command with persuasive AI response

### Core Modules
- **`callLLM.py`**: OpenRouter API integration using `openai/gpt-oss-20b:free` model
- **`Text_To_Speech.py`**: Piper TTS engine with GLaDOS voice model
- **`Speech_To_Text.py`**: Currently empty, uses RealtimeSTT library directly in Main.py
- **`Models/`**: Contains GLaDOS Piper voice model files (.onnx and .json config)

### Key Dependencies
- `RealtimeSTT.AudioToTextRecorder`: Real-time speech recognition
- `piper.PiperVoice`: Local TTS synthesis with ONNX models
- `sounddevice`: Audio playback for both tones and TTS output
- `requests`: OpenRouter API communication
- `onnxruntime`: Required for Piper TTS (imported but not directly used)

## Development Patterns

### Voice Model Configuration
- GLaDOS voice stored in `Models/glados_piper_medium.onnx`
- Synthesis config: `volume=1, length_scale=1, noise_scale=0, noise_w_scale=0`
- Sample rate: 22050 Hz, mono, int16 output

### API Integration
- OpenRouter API key hardcoded in `callLLM.py` (line 7)
- Default max_tokens: 300, overrideable per call
- Returns tuple: (content, message_object)

### Audio Processing
- Uses `sounddevice.OutputStream` for real-time audio playback
- Audio chunks processed as int16 numpy arrays
- Notification tone: 440Hz, 0.3s duration at 20% volume

### Conversation Management
- System prompt enforces plain text responses only
- GLaDOS persona defined in system messages
- Message history maintained in list format for API calls

## File Structure Conventions
- Main application logic in `Main.py`
- Separate modules for each major component
- Model files in `Models/` directory
- Empty `Speech_To_Text.py` indicates planned refactoring

## Testing
- `test.py` contains basic LLM integration testing
- Focuses on asterisk removal from AI responses
- Uses same message format as main application

## Environment Setup
- Python 3.13.7 virtual environment (`.venv/`)
- No requirements.txt - dependencies managed manually
- Windows-specific paths in model loading (`Models//` double slash)