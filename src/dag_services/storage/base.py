from abc import ABC, abstractmethod
from typing import Dict, List

class DAGStorage(ABC):
    """Base class for DAG storage"""
    
    @abstractmethod
    def save(self, name: str, dag: Dict) -> None:
        """Save a DAG"""
        pass
    
    @abstractmethod
    def load(self, name: str) -> Dict:
        """Load a DAG"""
        pass
    
    @abstractmethod
    def list(self) -> List[str]:
        """List all saved DAGs"""
        pass
    
    @abstractmethod
    def delete(self, name: str) -> None:
        """Delete a DAG"""
        pass