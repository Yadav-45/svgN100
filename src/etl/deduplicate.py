import sqlite3
import csv
from pathlib import Path

DB_PATH = Path("db/nifty100.db")
OUTPUT_DIR = Path("output")
REPORT_FILE = OUTPUT_DIR / "duplicate_report.csv"


def classify_duplicates(connection, table_name):
    results = []

    duplicate_groups = connection.execute(
        f"""
        SELECT company_id, year, COUNT(*) AS record_count
        FROM {table_name}
        GROUP BY company_id, year
        HAVING COUNT(*) > 1
        ORDER BY company_id, year
        """
    ).fetchall()

    for company_id, year, record_count in duplicate_groups:

        rows = connection.execute(
            f"""
            SELECT *
            FROM {table_name}
            WHERE company_id = ?
              AND year = ?
            """,
            (company_id, year),
        ).fetchall()

        # Ignore ID when comparing records.
        values = [row[1:] for row in rows]

        if all(row == values[0] for row in values):
            duplicate_type = "EXACT_DUPLICATE"
            action = "REMOVE_REDUNDANT_ROWS"
        else:
            duplicate_type = "SOURCE_CONFLICT"
            action = "PRESERVE_AND_FLAG"

        results.append({
            "table_name": table_name,
            "company_id": company_id,
            "year": year,
            "record_count": record_count,
            "duplicate_type": duplicate_type,
            "action": action,
        })

    return results


def main():
    print("=" * 70)
    print("DUPLICATE DATA QUALITY REPORT")
    print("=" * 70)

    connection = sqlite3.connect(DB_PATH)

    all_results = []

    for table_name in [
        "profitandloss",
        "balancesheet",
        "financial_ratios",
    ]:
        results = classify_duplicates(connection, table_name)
        all_results.extend(results)

    connection.close()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    columns = [
        "table_name",
        "company_id",
        "year",
        "record_count",
        "duplicate_type",
        "action",
    ]

    with open(REPORT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\nDuplicate groups found: {len(all_results)}")
    print(f"Report created: {REPORT_FILE}")

    print("\nSummary:")

    exact = sum(
        1 for row in all_results
        if row["duplicate_type"] == "EXACT_DUPLICATE"
    )

    conflicts = sum(
        1 for row in all_results
        if row["duplicate_type"] == "SOURCE_CONFLICT"
    )

    print(f"  Exact duplicate groups: {exact}")
    print(f"  Source conflict groups: {conflicts}")

    print("\n" + "=" * 70)
    print("REPORT COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()