import re
from typing import Dict, Any

def resolve_inputs(inputs: Dict, results: Dict[str, Any]) -> Dict:
    """Resolve variable references like @{{node.path.to.value}}"""
    resolved = {}
    
    for key, value in inputs.items():
        if isinstance(value, str):
            pattern = r'@\{\{([^}]+)\}\}'
            matches = re.findall(pattern, value)
            resolved_value = value
            
            for match in matches:
                parts = match.split('.')
                node_id = parts[0]
                
                if node_id in results:
                    result = results[node_id]
                    
                    for part in parts[1:]:
                        if isinstance(result, dict):
                            result = result.get(part)
                            if result is None:
                                break
                        else:
                            result = None
                            break
                    
                    if result is not None:
                        resolved_value = resolved_value.replace(f'@{{{{{match}}}}}', str(result))
            
            resolved[key] = resolved_value
        else:
            resolved[key] = value
    
    return resolved