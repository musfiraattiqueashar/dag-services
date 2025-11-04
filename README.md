# Workflow DAG

Simple DAG-based workflow execution engine using LangGraph.

## Installation
```bash
pip install git+https://github.com/yourusername/workflow-dag.git
```

## Usage
```python
from composio import Composio
from workflow_dag import DAGExecutor, ComposioExecutor

# Initialize Composio client
client = Composio(api_key="your-api-key")

# Create executor and DAG executor
executor = ComposioExecutor(client=client, user_id="your-user-id")
dag_executor = DAGExecutor(executor=executor)

# Define your workflow
dag = {
    "nodes": [
        {
            "id": "n1",
            "tool": "GOOGLEMEET_CREATE_MEET",
            "inputs": {"title": "Team Meeting"}
        },
        {
            "id": "n2",
            "tool": "GMAIL_SEND_EMAIL",
            "inputs": {
                "recipient_email": "user@example.com",
                "subject": "Meeting Invitation",
                "body": "Join: @{{n1.data.response_data.meetingUri}}"
            },
            "depends_on": ["n1"]
        }
    ]
}

# Execute
results = dag_executor.execute(dag)
print(results)
```

## Variable Resolution

Reference previous node outputs using `@{{node_id.path.to.value}}` syntax.

Example: `@{{n1.data.response_data.meetingUri}}` accesses the meeting URI from node n1.

## DAG Structure

Each node requires:
- `id`: Unique identifier
- `tool`: Composio tool name
- `inputs`: Tool input parameters
- `depends_on`: (optional) List of node IDs that must complete first

## Status

Custom executors and DAG storage are under construction.