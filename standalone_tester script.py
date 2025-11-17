from typing import Any
from composio import Composio, after_execute
from src.dag_services import DAGExecutor, ComposioExecutor, FileDAGStorage
# from config import COMPOSIO_API_KEY
from test_node_configs import sample_dags

# Initialize Composio client once
composio_client = Composio(api_key="ak_bbAtsAZnRudJjKDwkXAL")

# Pass the client instance to executor
executor = ComposioExecutor(client=composio_client, user_id="pg-test-1e717bc3-c2ac-45ed-bdee-0e23ee73680e")
storage = FileDAGStorage("./workflows")

# Create DAG executor
dag_executor = DAGExecutor(executor=executor, storage=None)


@after_execute(toolkits=['gmail'])
def minimal_response_modifier(tool: str, inputs: dict, result: Any) -> Any:
    """A simple modifier that trims the response to first 100 characters if it's a string."""
    if isinstance(result, str):
        return result[:100] + "..." if len(result) > 100 else result
    return result

modifiers = ['minimal_response_modifier']
for dag_config in sample_dags:
    results = dag_executor.execute(dag_config, )  # Pass the actual DAG config instead of a string
    with open(f"log_results_{dag_config['use_case']}.json", "w", encoding="utf-8") as f:
        import json
        json.dump(results, f, indent=2, default=str)
    print(f"Results for use case '{dag_config['use_case']}': {results}")