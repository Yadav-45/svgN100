from pathlib import Path
import csv
from datetime import datetime

OUTPUT_DIR = Path("output")
AUDIT_FILE = OUTPUT_DIR / "load_audit.csv"


def create_audit_report(load_results):
    """Create a CSV audit report for the ETL loading process."""

    OUTPUT_DIR.mkdir(exist_ok=True)

    fieldnames = [
        "timestamp",
        "table_name",
        "source_file",
        "rows_read",
        "rows_loaded",
        "duplicates_removed",
        "status",
    ]

    timestamp = datetime.now().isoformat(timespec="seconds")

    with open(AUDIT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for result in load_results:
            writer.writerow({
                "timestamp": timestamp,
                "table_name": result.get("table_name", ""),
                "source_file": result.get("source_file", ""),
                "rows_read": result.get("rows_read", 0),
                "rows_loaded": result.get("rows_loaded", 0),
                "duplicates_removed": result.get("duplicates_removed", 0),
                "status": result.get("status", "SUCCESS"),
            })

    print(f"✓ Load audit report created: {AUDIT_FILE}")