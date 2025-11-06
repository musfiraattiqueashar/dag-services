from typing import Dict

def validate_dag(dag: Dict) -> bool:
    """Validate DAG structure"""
    nodes = {n["id"]: n for n in dag["nodes"]}
    
    # Check dependencies exist
    for node in dag["nodes"]:
        for dep in node.get("depends_on", []):
            if dep not in nodes:
                print(f"❌ Node {node['id']} depends on non-existent node {dep}")
                return False
    
    # Check for cycles
    def has_cycle(node_id, visited, rec_stack):
        visited.add(node_id)
        rec_stack.add(node_id)
        
        for dep in nodes[node_id].get("depends_on", []):
            if dep not in visited:
                if has_cycle(dep, visited, rec_stack):
                    return True
            elif dep in rec_stack:
                print(f"❌ Circular dependency detected involving {node_id}")
                return True
        
        rec_stack.remove(node_id)
        return False
    
    visited = set()
    for node_id in nodes:
        if node_id not in visited:
            if has_cycle(node_id, set(), set()):
                return False
    
    # Check required fields
    for node in dag["nodes"]:
        if "id" not in node or "tool" not in node or "inputs" not in node:
            print(f"❌ Node missing required fields")
            return False
    
    print("DAG validation passed")
    return True