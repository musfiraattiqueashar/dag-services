from abc import ABC, abstractmethod
from typing import Dict, Any

class ToolExecutor(ABC):
    """Base class for tool executors"""
    
    @abstractmethod
    def execute(self, tool: str, inputs: Dict[str, Any]) -> Any:
        """Execute a tool with given inputs"""
        pass