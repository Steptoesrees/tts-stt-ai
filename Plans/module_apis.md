# VRChat AI Bot - Module API Contracts

## Core Module Interfaces

### 1. Configuration Manager
```python
class ConfigurationManager:
    def __init__(self, config_path: str = "config.yaml")
    def get(self, key: str, default: Any = None) -> Any
    def set(self, key: str, value: Any) -> None
    def load() -> bool
    def save() -> bool
    def validate() -> bool
```

### 2. State Manager
```python
class StateManager:
    def __init__(self, config: ConfigurationManager)
    def update_conversation_state(self, user_input: str, ai_response: str) -> None
    def get_conversation_context(self, max_turns: int = 10) -> List[Dict]
    def update_world_context(self, world_data: WorldData) -> None
    def get_avatar_state(self) -> AvatarState
    def set_avatar_state(self, state: AvatarState) -> None
```

### 3. Input Router
```python
class InputRouter:
    def __init__(self, state_manager: StateManager, config: ConfigurationManager)
    def register_input_handler(self, input_type: InputType, handler: Callable) -> None
    def route_input(self, input_data: InputData) -> Optional[ProcessedInput]
    def get_input_priority(self, input_data: InputData) -> int
```

## Input Layer APIs

### 4. Speech-to-Text Module
```python
class SpeechToTextModule:
    def __init__(self, config: ConfigurationManager, state_manager: StateManager)
    def start_listening(self) -> bool
    def stop_listening(self) -> bool
    def set_callback(self, callback: Callable[[str], None]) -> None
    def get_audio_devices(self) -> List[AudioDevice]
    def set_input_device(self, device_id: int) -> bool
```

### 5. OSC Event Listener
```python
class OSCEventListener:
    def __init__(self, config: ConfigurationManager, state_manager: StateManager)
    def start_listening(self, port: int = 9001) -> bool
    def stop_listening(self) -> bool
    def register_handler(self, address: str, handler: Callable) -> None
    def get_avatar_parameters(self) -> Dict[str, Any]
```

### 6. Computer Vision Module
```python
class ComputerVisionModule:
    def __init__(self, config: ConfigurationManager, state_manager: StateManager)
    def start_capture(self) -> bool
    def stop_capture(self) -> bool
    def get_world_map(self) -> WorldMap
    def detect_avatars(self) -> List[AvatarDetection]
    def get_depth_data(self) -> DepthData
```

## Processing Layer APIs

### 7. Prompt Generator
```python
class PromptGenerator:
    def __init__(self, config: ConfigurationManager, state_manager: StateManager)
    def generate_context_prompt(self, user_input: str, context: Dict) -> List[Dict]
    def add_world_context(self, world_data: WorldData) -> None
    def add_avatar_context(self, avatar_state: AvatarState) -> None
    def get_system_prompt(self) -> str
```

### 8. LLM Interface
```python
class LLMInterface:
    def __init__(self, config: ConfigurationManager)
    def generate_response(self, messages: List[Dict], max_tokens: int = 300) -> LLMResponse
    def set_model(self, model_name: str) -> bool
    def get_available_models(self) -> List[str]
    def validate_response(self, response: str) -> bool
```

## Output Layer APIs

### 9. Text-to-Speech Module
```python
class TextToSpeechModule:
    def __init__(self, config: ConfigurationManager)
    def speak(self, text: str, voice_model: str = None) -> bool
    def stop_speaking(self) -> bool
    def get_available_voices(self) -> List[Voice]
    def set_output_device(self, device_id: int) -> bool
    def is_speaking(self) -> bool
```

### 10. OSC Command Sender
```python
class OSCCommandSender:
    def __init__(self, config: ConfigurationManager)
    def send_chat_message(self, message: str, immediate: bool = True) -> bool
    def send_avatar_parameter(self, parameter: str, value: Any) -> bool
    def send_gesture(self, gesture: Gesture) -> bool
    def send_expression(self, expression: Expression) -> bool
```

### 11. VRChat API Module
```python
class VRChatAPIModule:
    def __init__(self, config: ConfigurationManager, state_manager: StateManager)
    def login(self, username: str, password: str) -> bool
    def get_friend_requests(self) -> List[FriendRequest]
    def accept_friend_request(self, request_id: str) -> bool
    def send_notification(self, user_id: str, message: str) -> bool
    def get_current_user(self) -> Optional[User]
```

## Data Structures

### Input Data Types
```python
@dataclass
class InputData:
    type: InputType  # SPEECH, OSC_EVENT, CV_DETECTION
    source: str
    timestamp: float
    data: Dict[str, Any]
    priority: int

@dataclass
class ProcessedInput:
    original_data: InputData
    processed_text: str
    context: Dict[str, Any]
    requires_response: bool
```

### World and Avatar Data
```python
@dataclass
class WorldData:
    world_id: str
    world_name: str
    player_count: int
    objects: List[WorldObject]
    avatars: List[AvatarInfo]

@dataclass
class AvatarState:
    position: Tuple[float, float, float]
    rotation: Tuple[float, float, float, float]
    gestures: Dict[str, bool]
    expressions: Dict[str, float]
    parameters: Dict[str, Any]
```

### LLM Response
```python
@dataclass
class LLMResponse:
    text: str
    raw_response: str
    tokens_used: int
    processing_time: float
    suggested_actions: List[Action]
```

## Error Handling Contracts

### Error Types
```python
class BotError(Exception):
    pass

class AudioError(BotError):
    pass

class OSCError(BotError):
    pass

class LLMError(BotError):
    pass

class VRChatAPIError(BotError):
    pass
```

### Recovery Strategies
- **Audio errors**: Retry with different device, fallback to text-only
- **OSC errors**: Reconnect, validate VRChat OSC settings
- **LLM errors**: Retry with backup model, use cached responses
- **Network errors**: Exponential backoff, offline mode