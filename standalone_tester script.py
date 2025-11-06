from composio import Composio
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


for dag_config in sample_dags:
    results = dag_executor.execute(dag_config)  # Pass the actual DAG config instead of a string
    print(f"Results for use case '{dag_config['use_case']}': {results}")