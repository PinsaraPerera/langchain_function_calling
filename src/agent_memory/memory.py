from pydantic import BaseModel
from typing import List, Union
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage

class AIChatMessage(BaseModel):
    content: str
    role: str = "AI"

class HumanChatMessage(BaseModel):
    content: str
    role: str = "Human"

class ToolChatMessage(BaseModel):
    content: str
    role: str = "Tool"

class ChatHistory(BaseModel):
    messages: List[Union[HumanMessage, AIMessage, ToolMessage]]

class Memory:
    def __init__(self):
        self.memory_store = {}

    def get_session_history(self, session_id: str) -> ChatHistory:
        """Retrieve session history or create a new one if it doesn't exist."""
        if session_id not in self.memory_store:
            self.memory_store[session_id] = ChatHistory(messages=[])
        return self.memory_store[session_id]
    
    def add_message(self, session_id: str, message: Union[AIChatMessage, HumanChatMessage, ToolChatMessage]):
        """Add a message to the session history."""
        if session_id not in self.memory_store:
            self.memory_store[session_id] = ChatHistory(messages=[])

        # Only add messages with content
        if message.content:
            self.memory_store[session_id].messages.append(message)

    def clear(self, session_id: str):
        """Clear the session history."""
        if session_id in self.memory_store:
            self.memory_store[session_id].messages = []
