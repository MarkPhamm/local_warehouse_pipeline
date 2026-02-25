"""
dlt Pipeline for CFPB Consumer Complaints

This pipeline extracts consumer complaint data from the CFPB API
and loads it into DuckDB in the raw schema.
"""

import hashlib
import logging
import re
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from typing import Any

import dlt
import pyarrow as pa
import pyarrow.parquet as pq
from dlt.destinations import duckdb

from ..apis.cfpb_api_client import CFPBAPIClient

logger = logging.getLogger(__name__)


@dlt.resource(
    name="cfpb_complaints",
    write_disposition="merge",
    primary_key="complaint_id",
)
def extract_complaints(
    date_received_min: str | None = None,
    date_received_max: str | None = None,
    company_name: str | None = None,
    max_records: int | None = None,
) -> Iterator[dict[str, Any]]:
    """
    Extract complaints from CFPB API.

    Args:
        date_received_min: Minimum received date (YYYY-MM-DD)
        date_received_max: Maximum received date (YYYY-MM-DD)
        company_name: Optional company name filter
        max_records: Maximum number of records to fetch

    Yields:
        Complaint records from the API
    """
    client = CFPBAPIClient()

    try:
        if company_name:
            logger.info(f"Extracting complaints for company: {company_name}")
            complaints = client.get_complaints_by_company(
                company_name=company_name,
                date_received_min=date_received_min,
                date_received_max=date_received_max,
                max_records=max_records,
            )
        else:
            logger.info("Extracting all complaints")
            complaints = client.get_complaints_paginated(
                date_received_min=date_received_min,
                date_received_max=date_received_max,
                max_records=max_records,
            )

        # Add extraction metadata
        extraction_timestamp = datetime.now().isoformat()

        for complaint in complaints:
            # Ensure complaint_id exists for primary key
            # The API may return _id or id fields - use those to construct complaint_id
            if "complaint_id" not in complaint or not complaint.get("complaint_id"):
                # Try to get ID from various possible fields (API returns _source with _id)
                complaint_id_field = (
                    complaint.get("_id") or complaint.get("id") or complaint.get("complaint_id")
                )

                # If we have an ID, use it; otherwise construct from date + hash
                if complaint_id_field:
                    complaint["complaint_id"] = str(complaint_id_field)
                else:
                    # Fallback: use date_received + hash of complaint data
                    date_received = complaint.get("date_received", "")
                    complaint_str = str(sorted(complaint.items()))
                    complaint_hash = hashlib.md5(complaint_str.encode()).hexdigest()[:8]
                    complaint["complaint_id"] = f"{date_received}_{complaint_hash}"

            # Add extraction metadata
            complaint["_dlt_extracted_at"] = extraction_timestamp

            yield complaint

    finally:
        client.close()


def _sanitize_filename(name: str) -> str:
    """Sanitize a string for use in filenames."""
    return re.sub(r"[^a-z0-9_]", "_", name.lower().strip())


def save_to_parquet(
    date_received_min: str,
    date_received_max: str,
    company_name: str,
    landing_dir: str = "landing/cfpb_complaints",
    max_records: int | None = None,
) -> str | None:
    """
    Extract complaints from the CFPB API and save as a parquet file.

    Args:
        date_received_min: Minimum received date (YYYY-MM-DD)
        date_received_max: Maximum received date (YYYY-MM-DD)
        company_name: Company name to filter
        landing_dir: Directory to write parquet files
        max_records: Maximum number of records to fetch

    Returns:
        Path to the written parquet file, or None if no records were extracted.
    """
    records = list(
        extract_complaints(
            date_received_min=date_received_min,
            date_received_max=date_received_max,
            company_name=company_name,
            max_records=max_records,
        )
    )

    if not records:
        logger.info(f"No records extracted for {company_name}, skipping parquet write")
        return None

    table = pa.Table.from_pylist(records)

    today_dir = datetime.now().strftime("%Y_%m_%d")
    landing_path = Path(landing_dir) / today_dir
    landing_path.mkdir(parents=True, exist_ok=True)

    safe_company = _sanitize_filename(company_name)
    filename = f"{safe_company}_{date_received_min}_{date_received_max}.parquet"
    file_path = landing_path / filename

    pq.write_table(table, file_path)
    logger.info(f"Wrote {len(records)} records to {file_path}")
    return str(file_path)


def load_parquet_to_duckdb(
    parquet_path: str,
    database_path: str = "database/cfpb_complaints.duckdb",
    schema_name: str = "raw",
) -> dict[str, Any]:
    """
    Load a parquet file into DuckDB via dlt (preserves merge/dedup logic).

    Args:
        parquet_path: Path to the parquet file to load
        database_path: Path to DuckDB database file
        schema_name: Schema name for the data

    Returns:
        Dictionary with load info
    """
    table = pq.read_table(parquet_path)
    records = table.to_pylist()
    logger.info(f"Read {len(records)} records from {parquet_path}")

    pipeline = create_pipeline(database_path=database_path, schema_name=schema_name)

    @dlt.resource(
        name="cfpb_complaints",
        write_disposition="merge",
        primary_key="complaint_id",
    )
    def parquet_source() -> Iterator[dict[str, Any]]:
        yield from records

    info = pipeline.run(parquet_source())
    logger.info(f"Loaded {len(records)} records from parquet into DuckDB")
    return {"records_loaded": len(records), "info": str(info)}


def create_pipeline(
    database_path: str = "database/cfpb_complaints.duckdb",
    schema_name: str = "raw",
) -> dlt.Pipeline:
    """
    Create and configure the dlt pipeline for CFPB complaints.

    Args:
        database_path: Path to DuckDB database file
        schema_name: Schema name for the data (default: raw)

    Returns:
        Configured dlt pipeline
    """
    # Ensure database directory exists
    db_path = Path(database_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Create pipeline
    # DuckDB destination accepts database path as string or in credentials dict
    pipeline = dlt.pipeline(
        pipeline_name="cfpb_complaints",
        destination=duckdb(credentials=str(db_path.absolute())),
        dataset_name=schema_name,
    )

    return pipeline
