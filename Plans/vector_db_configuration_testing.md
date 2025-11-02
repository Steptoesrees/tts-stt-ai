# Vector DB Memory System - Configuration & Testing

## Configuration System

### Core Configuration Structure

```yaml
# config/memory_config.yaml
memory_system:
  # Vector Database Configuration
  vector_db:
    type: "chromadb"  # Options: chromadb, qdrant, weaviate
    persist_directory: "./memory_db"
    collection_name: "ai_memories"
    settings:
      chroma_db_impl: "duckdb+parquet"
      anonymized_telemetry: false
    
  # Embedding Configuration
  embedding:
    model: "all-MiniLM-L6-v2"  # Default sentence-transformers model
    cache_embeddings: true
    cache_size: 1000
    batch_size: 32
    fallback_models:
      - "paraphrase-MiniLM-L3-v2"
      - "distiluse-base-multilingual-cased"
    
  # Retrieval Configuration
  retrieval:
    default_limit: 5
    max_context_length: 2000  # Characters for prompt context
    similarity_threshold: 0.7
    temporal_weight: 0.3      # Weight for recent memories
    importance_weight: 0.4    # Weight for important memories
    semantic_weight: 0.3      # Weight for semantic similarity
    
  # Memory Lifecycle Configuration
  lifecycle:
    importance_threshold: 0.2
    max_memories: 10000
    prune_interval_hours: 24
    backup_interval_hours: 6
    compression_enabled: true
    compression_threshold_days: 30
    
  # Integration Configuration
  integration:
    auto_create_conversation_memories: true
    max_memories_per_conversation: 10
    emotional_tone_detection: true
    topic_extraction: true
    
  # Performance Configuration
  performance:
    async_operations: true
    embedding_cache_ttl: 3600  # 1 hour
    max_concurrent_searches: 5
    memory_usage_monitoring: true
    
  # Error Handling Configuration
  error_handling:
    max_retry_attempts: 3
    retry_delay_seconds: 1
    fallback_to_keyword_search: true
    graceful_degradation: true
```

### Environment-Specific Configurations

```yaml
# config/development.yaml
memory_system:
  vector_db:
    persist_directory: "./dev_memory_db"
  performance:
    async_operations: false  # Easier debugging
  retrieval:
    default_limit: 3  # Smaller for testing

# config/production.yaml  
memory_system:
  vector_db:
    persist_directory: "/var/lib/ai_bot/memory_db"
  performance:
    async_operations: true
    max_concurrent_searches: 10
  lifecycle:
    max_memories: 50000

# config/testing.yaml
memory_system:
  vector_db:
    persist_directory: ":memory:"  # In-memory for tests
  embedding:
    cache_embeddings: false  # Fresh embeddings for each test
```

## Testing Strategy

### Unit Testing

```python
# tests/unit/test_memory_models.py
import pytest
from datetime import datetime
from src.memory.memory_models import Memory, ConversationMemory, MemoryType

class TestMemoryModels:
    def test_memory_creation(self):
        memory = Memory(
            id="test_1",
            type=MemoryType.CONVERSATION,
            content="Test conversation",
            metadata={"test": True},
            timestamp=datetime.now(),
            importance_score=0.5
        )
        assert memory.id == "test_1"
        assert memory.type == MemoryType.CONVERSATION
    
    def test_conversation_memory_metadata(self):
        memory = ConversationMemory(
            id="conv_1",
            content="User: Hello\nAI: Hi there!",
            speaker="user+ai",
            emotional_tone="friendly",
            conversation_topic="greeting",
            response_quality=0.8,
            metadata={},
            timestamp=datetime.now(),
            importance_score=0.0
        )
        assert memory.metadata["speaker"] == "user+ai"
        assert memory.metadata["emotional_tone"] == "friendly"

# tests/unit/test_memory_manager.py
class TestMemoryManager:
    def setup_method(self):
        self.manager = MemoryManager(test_config)
    
    def test_store_and_retrieve_memory(self):
        memory = create_test_memory()
        memory_id = self.manager.store_memory(memory)
        
        retrieved = self.manager.get_memory(memory_id)
        assert retrieved.content == memory.content
    
    def test_semantic_search(self):
        # Store multiple test memories
        memories = create_test_memories()
        for memory in memories:
            self.manager.store_memory(memory)
        
        # Search for relevant memories
        results = self.manager.search_memories("hello", limit=2)
        assert len(results) == 2
        assert results[0].similarity_score > 0.5
```

### Integration Testing

```python
# tests/integration/test_state_manager_integration.py
class TestStateManagerIntegration:
    def test_automatic_memory_creation(self):
        state_manager = EnhancedStateManager(config, memory_manager)
        
        # Simulate conversation
        state_manager.update_conversation_state(
            "Hello, how are you?", 
            "I'm doing well, thanks for asking!"
        )
        
        # Check if memory was created
        memories = memory_manager.search_memories("hello")
        assert len(memories) > 0
        assert memories[0].type == MemoryType.CONVERSATION

# tests/integration/test_prompt_generator_integration.py
class TestPromptGeneratorIntegration:
    def test_memory_context_in_prompts(self):
        prompt_generator = MemoryEnhancedPromptGenerator(
            config, state_manager, memory_manager
        )
        
        # Store some test memories
        store_test_memories(memory_manager)
        
        # Generate prompt
        prompt = prompt_generator.generate_context_prompt(
            "What did we talk about yesterday?",
            {}
        )
        
        # Check if memory context is included
        system_message = prompt[0]
        assert "Relevant Past Experiences" in system_message['content']
```

### Performance Testing

```python
# tests/performance/test_memory_performance.py
class TestMemoryPerformance:
    def test_memory_retrieval_latency(self):
        """Test that memory retrieval meets performance requirements"""
        # Store large number of memories
        memories = generate_large_memory_set(1000)
        for memory in memories:
            memory_manager.store_memory(memory)
        
        # Measure retrieval time
        start_time = time.time()
        results = memory_manager.search_memories("test query", limit=5)
        end_time = time.time()
        
        retrieval_time = end_time - start_time
        assert retrieval_time < 0.1  # 100ms requirement
    
    def test_concurrent_operations(self):
        """Test performance under concurrent load"""
        import concurrent.futures
        
        def concurrent_operation(i):
            memory = create_test_memory(f"concurrent_{i}")
            return memory_manager.store_memory(memory)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(concurrent_operation, i) for i in range(100)]
            results = [f.result() for f in futures]
        
        assert len(results) == 100
```

### End-to-End Testing

```python
# tests/e2e/test_full_memory_system.py
class TestFullMemorySystem:
    def test_complete_memory_lifecycle(self):
        """Test complete memory system from creation to retrieval"""
        # Setup
        config = load_test_config()
        memory_manager = MemoryManager(config)
        state_manager = EnhancedStateManager(config, memory_manager)
        prompt_generator = MemoryEnhancedPromptGenerator(
            config, state_manager, memory_manager
        )
        
        # Simulate multiple conversations
        conversations = [
            ("I love pizza", "Pizza is delicious!"),
            ("What's your favorite food?", "I really enjoy Italian cuisine"),
            ("Tell me about pizza", "Pizza originated in Italy...")
        ]
        
        for user_input, ai_response in conversations:
            state_manager.update_conversation_state(user_input, ai_response)
        
        # Test memory retrieval and context enhancement
        prompt = prompt_generator.generate_context_prompt(
            "What food do you like?",
            {}
        )
        
        # Verify memory context is relevant
        system_message = prompt[0]['content']
        assert "pizza" in system_message.lower()
        assert "Italian" in system_message
        
        # Test memory pruning
        memory_manager.maintenance.prune_low_importance_memories()
        remaining_memories = memory_manager.get_all_memories()
        assert all(m.importance_score > 0.2 for m in remaining_memories)
```

## Error Handling and Recovery Strategies

### Error Classification

```python
# src/memory/error_handling.py
from enum import Enum

class MemoryErrorType(Enum):
    DATABASE_CONNECTION = "database_connection"
    EMBEDDING_GENERATION = "embedding_generation"
    MEMORY_CORRUPTION = "memory_corruption"
    STORAGE_LIMIT = "storage_limit"
    CONFIGURATION_ERROR = "configuration_error"

class MemorySystemError(Exception):
    def __init__(self, error_type: MemoryErrorType, message: str, original_error: Exception = None):
        self.error_type = error_type
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)

class EmbeddingError(MemorySystemError):
    pass

class DatabaseError(MemorySystemError):
    pass
```

### Recovery Strategies

```python
# src/memory/recovery_strategies.py
class RecoveryStrategies:
    def __init__(self, config: ConfigurationManager):
        self.config = config
        self.retry_count = 0
        self.max_retries = config.get('memory_system.error_handling.max_retry_attempts', 3)
    
    def handle_embedding_failure(self, text: str, original_error: Exception) -> List[float]:
        """Handle embedding generation failures"""
        self.retry_count += 1
        
        if self.retry_count <= self.max_retries:
            # Retry with exponential backoff
            delay = 2 ** self.retry_count
            time.sleep(delay)
            return self._retry_embedding(text)
        else:
            # Fallback strategies
            return self._fallback_embedding(text)
    
    def _fallback_embedding(self, text: str) -> List[float]:
        """Provide fallback embedding when primary method fails"""
        # Strategy 1: Use simpler embedding model
        try:
            from sentence_transformers import SentenceTransformer
            fallback_model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
            return fallback_model.encode(text).tolist()
        except:
            pass
        
        # Strategy 2: Use keyword-based pseudo-embedding
        return self._keyword_based_embedding(text)
    
    def handle_database_failure(self, operation: str, original_error: Exception):
        """Handle database connection failures"""
        if "connection" in str(original_error).lower():
            return self._reconnect_database()
        elif "corruption" in str(original_error).lower():
            return self._repair_database()
        else:
            raise DatabaseError(
                MemoryErrorType.DATABASE_CONNECTION,
                f"Database operation failed: {operation}",
                original_error
            )
    
    def _reconnect_database(self) -> bool:
        """Attempt to reconnect to database"""
        try:
            # Close existing connection
            if hasattr(self, 'client'):
                self.client.close()
            
            # Reinitialize
            self.client = chromadb.Client(self.settings)
            self.collection = self.client.get_collection("ai_memories")
            return True
        except Exception as e:
            return False
    
    def _repair_database(self) -> bool:
        """Attempt to repair corrupted database"""
        try:
            # Create backup
            self._create_backup()
            
            # Rebuild from backup or scratch
            if self._can_recover_from_backup():
                return self._restore_from_backup()
            else:
                return self._rebuild_database()
        except Exception as e:
            return False
```

### Graceful Degradation

```python
# src/memory/graceful_degradation.py
class GracefulDegradation:
    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager
        self.degradation_level = 0  # 0 = full functionality, 1 = limited, 2 = minimal
    
    def get_relevant_memories(self, query: str, context: Dict) -> List[Memory]:
        """Get memories with graceful degradation"""
        try:
            if self.degradation_level == 0:
                # Full semantic search
                return self.memory_manager.search_memories(query, limit=5)
            elif self.degradation_level == 1:
                # Limited search (recent memories only)
                return self.memory_manager.get_recent_memories(hours=24, limit=3)
            else:
                # Minimal functionality (no memories)
                return []
        except Exception as e:
            # Further degrade on error
            self.degradation_level = min(self.degradation_level + 1, 2)
            return self.get_relevant_memories(query, context)  # Retry with degraded mode
    
    def should_create_memory(self, memory_data: Dict) -> bool:
        """Determine if memory should be created based on degradation level"""
        if self.degradation_level >= 2:
            return False  # Don't create new memories in minimal mode
        
        # Only create important memories in limited mode
        if self.degradation_level == 1:
            importance = self._estimate_importance(memory_data)
            return importance > 0.7
        
        return True  # Create all memories in full mode
```

## Testing Configuration

### pytest Configuration

```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --color=yes
    --cov=src/memory
    --cov-report=html
    --cov-report=term-missing
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: integration tests
    performance: performance tests
```

### Test Data Generation

```python
# tests/utils/test_data_generator.py
class TestDataGenerator:
    @staticmethod
    def generate_conversation_memories(count: int) -> List[ConversationMemory]:
        """Generate realistic conversation memories for testing"""
        conversations = [
            ("Hello there!", "Hi! How are you doing today?"),
            ("I'm good, thanks!", "That's great to hear!"),
            ("What's your favorite color?", "I really like blue, it's so calming."),
            ("Tell me about yourself", "I'm an AI assistant here to help and chat with you!"),
            ("Do you like music?", "I enjoy all kinds of music! What about you?"),
        ]
        
        memories = []
        for i in range(count):
            user_msg, ai_msg = conversations[i % len(conversations)]
            memory = ConversationMemory(
                id=f"test_conv_{i}",
                content=f"User: {user_msg}\nAI: {ai_msg}",
                speaker="user+ai",
                emotional_tone=random.choice(["friendly", "excited", "calm", "curious"]),
                conversation_topic=random.choice(["greeting", "personal", "hobbies", "general"]),
                response_quality=random.uniform(0.5, 1.0),
                metadata={"test": True},
                timestamp=datetime.now() - timedelta(hours=random.randint(0, 168)),
                importance_score=random.uniform(0.1, 1.0)
            )
            memories.append(memory)
        
        return memories
```

This comprehensive configuration and testing strategy ensures the vector DB memory system is robust, well-tested, and can handle various error conditions gracefully while maintaining performance.