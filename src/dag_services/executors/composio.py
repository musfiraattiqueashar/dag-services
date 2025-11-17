from typing import Dict, Any, List
from .base import ToolExecutor

class ComposioExecutor(ToolExecutor):
    """Composio tool executor"""
    
    def __init__(self, client, user_id: str):
        """
        Args:
            client: Composio client instance
            user_id: Composio user ID
        """
        self.client = client
        self.user_id = user_id
    
    def execute(self, tool: str, inputs: Dict[str, Any], modifiers: List[str]) -> Any:
        return self.client.tools.execute(
            slug=tool,
            arguments=inputs,
            user_id=self.user_id,
            dangerously_skip_version_check=True,
            modifiers=modifiers

        )
    
    