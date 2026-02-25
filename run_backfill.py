#!/usr/bin/env python3
"""
Backfill the landing area with daily parquet files.

Creates one directory per day under landing/cfpb_complaints/YYYY_MM_DD/
with a parquet file per company (including empty files for days with no data).

Usage:
    # Backfill a date range
    python run_backfill.py --start 2026-01-01 --end 2026-02-25

    # Backfill a single day
    python run_backfill.py --start 2026-01-15 --end 2026-01-15

    # Backfill last 7 days
    python run_backfill.py --days 7
"""

import argparse
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.cfg.config import COMPANIES
from src.pipelines.cfpb_complaints_pipeline import save_to_parquet

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def backfill(start_date: datetime, end_date: datetime) -> dict:
    """
    Backfill the landing area for a date range.

    Args:
        start_date: First day to backfill (inclusive).
        end_date: Last day to backfill (inclusive).

    Returns:
        Summary dict with total_days, total_files, total_rows, and per-day details.
    """
    total_days = (end_date - start_date).days + 1
    logger.info(
        f"Backfilling {total_days} days ({start_date.date()} to {end_date.date()}) "
        f"for {len(COMPANIES)} companies"
    )

    daily_results = []
    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        next_day = (current + timedelta(days=1)).strftime("%Y-%m-%d")
        day_label = current.strftime("%Y_%m_%d")

        logger.info(f"--- {day_label} ---")
        day_files = []
        for company in COMPANIES:
            result = save_to_parquet(
                date_received_min=date_str,
                date_received_max=next_day,
                company_name=company,
                landing_date=date_str,
            )
            day_files.append(result)
            logger.info(f"  {company}: {result}")

        daily_results.append({"date": day_label, "files": len(day_files)})
        current += timedelta(days=1)

    total_files = total_days * len(COMPANIES)
    logger.info(f"Backfill complete: {total_days} days, {total_files} files")
    return {
        "total_days": total_days,
        "total_files": total_files,
        "daily_results": daily_results,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Backfill landing area with daily parquet files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run python run_backfill.py --start 2026-01-01 --end 2026-02-25
  uv run python run_backfill.py --start 2026-01-15 --end 2026-01-15
  uv run python run_backfill.py --days 7
        """,
    )
    parser.add_argument(
        "--start",
        type=str,
        help="Start date inclusive (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--end",
        type=str,
        default=datetime.now().strftime("%Y-%m-%d"),
        help="End date inclusive (YYYY-MM-DD, default: today)",
    )
    parser.add_argument(
        "--days",
        type=int,
        help="Backfill the last N days (alternative to --start)",
    )

    args = parser.parse_args()

    if args.days:
        end_date = datetime.strptime(args.end, "%Y-%m-%d")
        start_date = end_date - timedelta(days=args.days - 1)
    elif args.start:
        start_date = datetime.strptime(args.start, "%Y-%m-%d")
        end_date = datetime.strptime(args.end, "%Y-%m-%d")
    else:
        parser.error("Either --start or --days is required")

    if start_date > end_date:
        parser.error(f"Start date {start_date.date()} is after end date {end_date.date()}")

    backfill(start_date, end_date)
    return 0


if __name__ == "__main__":
    sys.exit(main())
