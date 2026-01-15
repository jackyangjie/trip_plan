from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from datetime import datetime


class AgentMessage(BaseModel):
    sender: str
    receiver: str
    content: Any
    timestamp: str
    message_type: str = "text"


class BaseAgent(ABC):
    name: str
    description: str

    def __init__(self):
        self.memory: List[AgentMessage] = []

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass


class AgentResult(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
