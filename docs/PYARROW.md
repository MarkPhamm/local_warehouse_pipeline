# Why PyArrow?

## Role in the Pipeline

PyArrow is used to write and read **Parquet files** in the landing area (`landing/cfpb_complaints/`). It serves as the bridge between API extraction and DuckDB loading.

```text
CFPB API → extract_complaints() → PyArrow writes Parquet → PyArrow reads Parquet → dlt loads to DuckDB
```

## Why Parquet?

- **Columnar format**: Efficient storage and fast analytical reads
- **Schema preservation**: Data types are encoded in the file, no CSV parsing ambiguity
- **Compression**: Parquet files are significantly smaller than JSON/CSV equivalents
- **DuckDB native support**: DuckDB can read Parquet files directly via `read_parquet()`

## Why PyArrow (vs alternatives)?

| Option      | Pros                                                                               | Cons                                           |
| ----------- | ---------------------------------------------------------------------------------- | ---------------------------------------------- |
| **PyArrow** | Zero new dependencies (transitive dep of dlt + duckdb), fast, full Parquet support | Slightly verbose API                           |
| pandas      | Familiar API                                                                       | Would add a heavy dependency just for file I/O |
| fastparquet | Lightweight                                                                        | Extra dependency, less maintained              |
| DuckDB COPY | No Python intermediary                                                             | Doesn't help with writing from API data        |

PyArrow is already installed as a transitive dependency of both `dlt` and `duckdb`, so it adds **zero additional packages** to the project.

## Usage in the Codebase

### Writing (`save_to_parquet`)

```python
import pyarrow as pa
import pyarrow.parquet as pq

table = pa.Table.from_pylist(records)
pq.write_table(table, file_path)
```

### Reading (`load_parquet_to_duckdb`)

```python
table = pq.read_table(parquet_path)
records = table.to_pylist()
```

## File Location

Parquet files are written to:

```text
landing/cfpb_complaints/{company}_{date_min}_{date_max}.parquet
```

These files are gitignored and serve as a local staging area for debugging, archival, and replayability.
