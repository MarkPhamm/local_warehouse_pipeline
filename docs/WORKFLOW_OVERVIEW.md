# CFPB Complaints Pipeline – Workflow Overview

---

## 1. Flow Entry  
**Function:** `cfpb_complaints_incremental_flow()`  
**File:** `src/orchestration/cfpb_flows.py`

This is the main Prefect flow. It:

- Determines the load window using `get_next_load_date()`  
  → **File:** `src/utils/state.py`
- Reads `COMPANIES` from config  
  → **File:** `src/cfg/config.py`
- Loops through each company and calls the Extract+Load task

---

## 2. Extract + Load (per company)

**Task:** `extract_and_load_complaints_task()`  
**File:** `src/orchestration/cfpb_flows.py`

Inside this task:

### ✔ `create_pipeline()`  
**File:** `src/pipelines/cfpb_complaints_pipeline.py`  
Creates/open DuckDB pipeline connection.

### ✔ `extract_complaints()`  
**File:** `src/pipelines/cfpb_complaints_pipeline.py`  
Calls the CFPB API to retrieve complaint records for:
- `date_min`
- `date_max`
- `company_name`

### ✔ `pipeline.run(...)`  
**File:** `src/pipelines/cfpb_complaints_pipeline.py`  
Loads extracted data into the DuckDB database:
`database/cfpb_complaints.duckdb`

This step handles **Extract → Load (EL)**.

---

## 3. Update Incremental State

If all companies completed successfully:

### ✔ `update_last_loaded_date(date_max)`
**File:** `src/utils/state.py`

Updates `pipeline_state.json`, enabling:
- Incremental loading on next run
- Avoiding reprocessing old data

---

## 4. Transform with dbt

**Task:** `run_dbt_models_task()`  
**File:** `src/orchestration/cfpb_flows.py`

Process SQL models by layers

## 5. Test with dbt

**Task:** `run_dbt_tests_task()`  
**File:** `src/orchestration/cfpb_flows.py`