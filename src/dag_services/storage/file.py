import json
import os
from pathlib import Path
from typing import Dict, List
from .base import DAGStorage

class FileDAGStorage(DAGStorage):
    """File-based DAG storage"""
    
    def __init__(self, directory: str = "./dags"):
        self.directory = Path(directory)
        self.directory.mkdir(exist_ok=True)
    
    def save(self, name: str, dag: Dict) -> None:
        filepath = self.directory / f"{name}.json"
        with open(filepath, 'w') as f:
            json.dump(dag, f, indent=2)
        print(f"✓ Saved DAG: {name}")
    
    def load(self, name: str) -> Dict:
        filepath = self.directory / f"{name}.json"
        if not filepath.exists():
            raise FileNotFoundError(f"DAG '{name}' not found")
        
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def list(self) -> List[str]:
        return [f.stem for f in self.directory.glob("*.json")]
    
    def delete(self, name: str) -> None:
        filepath = self.directory / f"{name}.json"
        if filepath.exists():
            filepath.unlink()
            print(f"✓ Deleted DAG: {name}")