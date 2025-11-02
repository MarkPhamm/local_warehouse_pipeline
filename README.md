# local_elt_pipeline

A local-first ELT pipeline that extracts CFPB consumer complaint data, transforms it with dbt into analytics-ready models, and serves interactive dashboards—all running on your laptop with zero cloud dependencies.
<img width="1200" height="500" alt="image" src="https://github.com/user-attachments/assets/a8752180-63af-4f0a-8e0e-a973188651ed" />

* **Package Manager**: uv (Python)
* **Ingestion**: dlt
* **Transformation**: dbt core
* **OLAP Database**: DuckDB
* **Orchestration**: Prefect
* **BI Tool**: Visivo

## 1. Quick Start

### 1.1 Setup

```bash
# Install dependencies
uv sync

# Install dev dependencies (for testing)
uv sync --extra dev
```

### 1.2 Configuration

Edit `src/cfg/config.py` to configure companies and start date:

```python
START_DATE = "2024-01-01"
COMPANIES = ["jpmorgan", "bank of america"]
```

### 1.3 Run the Pipeline

```bash
# Run incremental pipeline (first run loads from START_DATE to today)
uv run python run_prefect_flow.py

# Reset state to reload from START_DATE
uv run python run_prefect_flow.py --reset-state
```

### 1.4 Access Prefect UI (Optional)

```bash
# Start Prefect server
./start_prefect_server.sh

# Access UI at http://127.0.0.1:4200
```

### 1.5 Access DuckDB UI

First, install the DuckDB CLI:

```bash
# macOS (using Homebrew)
brew install duckdb

# Or download from https://duckdb.org/docs/installation/
```

Then launch the DuckDB UI:

```bash
duckdb -ui
```

Additional docs: [DuckDB UI Documentation](https://duckdb.org/docs/api/cli/ui)

### 1.6 Access Visivo Dashboards

Start the Visivo web server to view interactive dashboards:

```bash
# Navigate to visivo directory
cd visivo

# Start web server (runs on http://localhost:8080 by default)
uv run visivo serve

# Or use a custom port
uv run visivo serve --port 3000
```

Then open your browser to:

* **Dashboard URL**: <http://localhost:8080>

**Available Dashboards**:

* **Executive Dashboard**: High-level overview of complaint trends and company performance
* **Geographic Dashboard**: State-by-state complaint distribution and analysis

**Note**: Before viewing dashboards, ensure:

1. Data pipeline has been run (`uv run python run_prefect_flow.py`)
2. dbt models have been built (`cd duckdb_dbt && dbt run`)

Additional docs: [Visivo Documentation](docs/README_VISIVO.MD)

## 2. Testing

```bash
# Run python tests
uv run pytest tests/
```

```bash
# Run dbt tests
cd duckdb_dbt
dbt test
```

## 3. License

See [LICENSE](LICENSE) file for details.
