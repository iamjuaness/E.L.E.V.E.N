from src.brain.memory import MemoryManager
import os

def test_memory():
    print("Testing MemoryManager...")
    
    # Initialize
    mem = MemoryManager()
    
    # Add dummy data
    print("Adding messages...")
    mem.add_message("user", "Hello, do you remember me?")
    mem.add_message("model", "Yes, I remember you.")
    
    # Retrieve
    print("Retrieving history...")
    history = mem.get_recent_history(limit=2)
    
    for msg in history:
        print(f"Role: {msg['role']}, Content: {msg['parts'][0]}")
        
    # Check persistence
    assert len(history) >= 2
    print("Memory test passed!")

if __name__ == "__main__":
    test_memory()
