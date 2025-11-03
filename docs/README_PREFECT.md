# Prefect Orchestration Documentation

## 1. Overview

<img src="../images/prefect.png" alt="prefect" style="width:100%">

Prefect is a modern workflow orchestration platform used in this project to manage and monitor data pipeline execution. This project uses Prefect 3.x for workflow orchestration, providing task tracking, monitoring, automatic retry logic, centralized logging, and flow run history.

**Key Features:**

- **Task Tracking**: Monitor individual tasks within workflows
- **Automatic Retries**: Built-in retry logic for failed tasks
- **Centralized Logging**: All logs aggregated in one place
- **Flow Run History**: Track execution history and performance
- **Web UI**: Visual interface for monitoring and debugging
- **Scheduling**: Support for cron-based and cloud-based scheduling

## 2. Architecture

### 2.1 Flow Structure

```text
cfpb-complaints-incremental (Flow)
  ├── extract_and_load_complaints (Task)
  │   └── Per company extraction and loading
  └── run_dbt_models (Task)
      └── Transform data with dbt
```

### 2.2 Components

- **Flows**: Top-level workflow definitions (`@flow` decorator)
- **Tasks**: Individual units of work (`@task` decorator)
- **Prefect Server**: Local server for running and monitoring flows
- **Prefect UI**: Web interface at <http://127.0.0.1:4200>

## 3. Setup

### 3.1 Installation

Prefect is already included in the project dependencies:

```bash
uv sync
```

### 3.2 Starting Prefect Server

**Quick Start:**

```bash
# Start Prefect server
./start_prefect_server.sh

# Or manually:
uv run prefect server start

# Access UI at http://127.0.0.1:4200
```

**Running Server in Background:**

```bash
# Option 1: Background process
uv run prefect server start &

# Option 2: With nohup (persists after terminal closes)
nohup uv run prefect server start > prefect_server.log 2>&1 &

# Option 3: Using tmux
tmux new -s prefect
uv run prefect server start
# Press Ctrl+B then D to detach
```

## 4. Usage

### 4.1 Running Flows

The main pipeline flow is executed via:

```bash
# Run incremental pipeline (first run = initial load, subsequent = incremental)
uv run python run_prefect_flow.py

# Reset state to reload from START_DATE
uv run python run_prefect_flow.py --reset-state

# Custom database path
uv run python run_prefect_flow.py --database path/to/database.duckdb
```

### 4.2 Using the UI

1. Start Prefect server in one terminal
2. Run flows in another terminal - they appear automatically in the UI
3. Monitor: View flow runs, logs, task details, and execution history

**UI Features:**

- View all flow runs and their status
- Inspect task-level details and logs
- Monitor execution times and resource usage
- Debug failed runs with detailed error messages
- View flow run history and trends

## 5. Flow Definition

The main flow is defined in `src/orchestration/cfpb_flows.py`:

```python
@flow(name="cfpb-complaints-incremental")
def cfpb_complaints_incremental_flow(
    database_path: str = "database/cfpb_complaints.duckdb",
    reset_state: bool = False,
) -> dict[str, Any]:
    """
    Main Prefect flow for incremental CFPB complaints pipeline.
    
    Steps:
    1. Determine date range for extraction
    2. Extract and load complaints for each company
    3. Run dbt transformations
    4. Update state on success
    """
    # Flow implementation
```

## 6. Scheduling

### 6.1 Using Cron

For local scheduling, use cron:

```bash
# Add to crontab (crontab -e)
0 2 * * * cd /path/to/local_elt_pipeline && uv run python run_prefect_flow.py
```

### 6.2 Using Prefect Cloud

For production, you can use Prefect Cloud (free tier available):

```bash
# Sign up at https://app.prefect.cloud
# Login with API key
uv run prefect cloud login --key YOUR_API_KEY

# Deploy flows to Prefect Cloud
uv run prefect deploy
```

## 7. Monitoring and Observability

### 7.1 Flow Run Monitoring

- **Status**: Track flow runs as Running, Completed, Failed, or Cancelled
- **Logs**: View real-time and historical logs for each task
- **Metrics**: Monitor execution time, success rates, and resource usage
- **Alerts**: Set up notifications for failed runs (with Prefect Cloud)

### 7.2 Task Retries

Prefect automatically retries failed tasks based on configuration:

```python
@task(retries=3, retry_delay_seconds=60)
def my_task():
    # Task implementation
```

## 8. Troubleshooting

### 8.1 Common Issues

**Port Already in Use:**

```bash
uv run prefect server start --port 4201
```

**Server Won't Start:**

```bash
# Ensure dependencies are installed
uv sync
```

**Flows Not Appearing in UI:**

- Ensure Prefect server is running before executing flows
- Flows must be executed at least once to appear in UI
- Check that flows are using the correct Prefect server URL

### 8.2 Debugging

**View Flow Logs:**

- Use Prefect UI to view detailed logs
- Check console output when running flows directly
- Review `prefect_server.log` if running in background

**Check Flow Status:**

```bash
# List recent flow runs
uv run prefect flow-run ls

# View specific flow run details
uv run prefect flow-run inspect <flow-run-id>
```

## 9. Best Practices

1. **Use Flow Names**: Always name your flows for easy identification
2. **Task Granularity**: Break workflows into logical, reusable tasks
3. **Error Handling**: Implement proper error handling in tasks
4. **State Management**: Use Prefect state for tracking pipeline progress
5. **Logging**: Use Prefect's logging instead of print statements
6. **Resource Management**: Configure appropriate retries and timeouts

## 10. Additional Resources

- [Prefect Documentation](https://docs.prefect.io/)
- [Prefect Cloud](https://app.prefect.cloud)
- [Prefect GitHub](https://github.com/PrefectHQ/prefect)
