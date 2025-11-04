from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any, Annotated, Optional
import operator

from .validator import validate_dag
from .resolver import resolve_inputs
from ..executors.base import ToolExecutor
from ..storage.base import DAGStorage

class AgentState(TypedDict):
    results: Annotated[Dict[str, Any], operator.or_]

class DAGExecutor:
    def __init__(self, executor: ToolExecutor, storage: Optional[DAGStorage] = None):
        """
        Args:
            executor: Tool executor implementation
            storage: Optional DAG storage for save/load
        """
        self.executor = executor
        self.storage = storage
        self.execution_tracker = {}
    
    def execute(self, dag: Dict) -> Dict[str, Any]:
        """Execute a DAG and return results"""
        if not validate_dag(dag):
            raise ValueError("Invalid DAG")
        
        self.execution_tracker = {}
        graph = self._build_graph(dag)
        
        initial_state = {"results": {}}
        final_state = graph.invoke(initial_state)
        
        # Verify each node executed once
        for node in dag["nodes"]:
            count = self.execution_tracker.get(node["id"], 0)
            if count != 1:
                print(f"⚠️  Node {node['id']} executed {count} times (expected 1)")
        
        return final_state["results"]
    
    def execute_saved(self, name: str) -> Dict[str, Any]:
        """Execute a saved DAG by name"""
        if not self.storage:
            raise ValueError("No storage configured")
        
        dag = self.storage.load(name)
        return self.execute(dag)
    
    def save_dag(self, name: str, dag: Dict) -> None:
        """Save a DAG for later execution"""
        if not self.storage:
            raise ValueError("No storage configured")
        
        if not validate_dag(dag):
            raise ValueError("Invalid DAG")
        
        self.storage.save(name, dag)
    
    def _build_graph(self, dag: Dict) -> StateGraph:
        workflow = StateGraph(AgentState)
        
        # Add nodes
        for node in dag["nodes"]:
            workflow.add_node(node["id"], self._create_node_executor(node))
        
        # Set entry point
        root_nodes = [n["id"] for n in dag["nodes"] if not n.get("depends_on")]
        if root_nodes:
            workflow.set_entry_point(root_nodes[0])
        
        # Add edges
        for node in dag["nodes"]:
            node_id = node["id"]
            depends_on = node.get("depends_on", [])
            
            if depends_on:
                workflow.add_edge(depends_on[-1], node_id)
            
            has_dependents = any(node_id in n.get("depends_on", []) for n in dag["nodes"])
            if not has_dependents:
                workflow.add_edge(node_id, END)
        
        return workflow.compile()
    
    def _create_node_executor(self, node_config: Dict):
        def execute_node(state: AgentState) -> AgentState:
            node_id = node_config["id"]
            
            # Track execution
            if node_id not in self.execution_tracker:
                self.execution_tracker[node_id] = 0
            self.execution_tracker[node_id] += 1
            
            # Check dependencies
            depends_on = node_config.get("depends_on", [])
            if depends_on:
                completed = set(state["results"].keys())
                if not all(dep in completed for dep in depends_on):
                    return {"results": {}}
            
            # Resolve inputs and execute
            resolved_inputs = resolve_inputs(node_config["inputs"], state["results"])
            result = self.executor.execute(node_config["tool"], resolved_inputs)
            
            print(f"✓ Executed {node_id} ({node_config['tool']})")
            return {"results": {node_id: result}}
        
        return execute_node