import sqlite3
from pathlib import Path
import csv


DB_PATH = Path("db/nifty100.db")
OUTPUT_DIR = Path("output")
FAILURES_FILE = OUTPUT_DIR / "validation_failures.csv"


def add_failure(
    failures,
    rule_id,
    severity,
    table_name,
    record_id,
    company_id,
    year,
    message,
):
    failures.append({
        "rule_id": rule_id,
        "severity": severity,
        "table_name": table_name,
        "record_id": record_id,
        "company_id": company_id,
        "year": year,
        "message": message,
    })


def validate_positive_sales(connection, failures):
    """DQ-05: Sales must be greater than zero."""

    rows = connection.execute("""
        SELECT
            id,
            company_id,
            year,
            sales
        FROM profitandloss
        WHERE sales IS NULL
           OR sales <= 0
    """).fetchall()

    for row in rows:
        add_failure(
            failures=failures,
            rule_id="DQ-05",
            severity="CRITICAL",
            table_name="profitandloss",
            record_id=row[0],
            company_id=row[1],
            year=row[2],
            message=(
                f"Sales must be greater than zero. "
                f"Actual value: {row[3]}"
            ),
        )


def validate_foreign_keys(connection, failures):
    """DQ-03: Check SQLite foreign-key integrity."""

    rows = connection.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()

    for row in rows:
        add_failure(
            failures=failures,
            rule_id="DQ-03",
            severity="CRITICAL",
            table_name=row[0],
            record_id=row[1],
            company_id="",
            year="",
            message=f"Foreign-key violation: {row}",
        )


def validate_company_count(connection, failures):
    """DQ-01: Check that exactly 100 unique companies exist."""

    total = connection.execute(
        "SELECT COUNT(*) FROM companies"
    ).fetchone()[0]

    unique = connection.execute(
        "SELECT COUNT(DISTINCT id) FROM companies"
    ).fetchone()[0]

    if total != 100 or unique != 100:
        add_failure(
            failures=failures,
            rule_id="DQ-01",
            severity="CRITICAL",
            table_name="companies",
            record_id="",
            company_id="",
            year="",
            message=(
                f"Expected 100 unique companies. "
                f"Found {total} rows and {unique} unique IDs."
            ),
        )


def validate_duplicate_company_ids(connection, failures):
    """DQ-02: Check that company IDs are unique."""

    rows = connection.execute("""
        SELECT
            id,
            COUNT(*) AS duplicate_count
        FROM companies
        GROUP BY id
        HAVING COUNT(*) > 1
    """).fetchall()

    for row in rows:
        add_failure(
            failures=failures,
            rule_id="DQ-02",
            severity="CRITICAL",
            table_name="companies",
            record_id="",
            company_id=row[0],
            year="",
            message=(
                f"Duplicate company ID found. "
                f"Occurrences: {row[1]}"
            ),
        )


def validate_company_year_duplicates(connection, failures):
    """DQ-04: Check for duplicate company-year records."""

    tables = [
        "profitandloss",
        "balancesheet",
        "financial_ratios",
    ]

    for table_name in tables:
        rows = connection.execute(f"""
            SELECT
                company_id,
                year,
                COUNT(*) AS duplicate_count
            FROM {table_name}
            GROUP BY company_id, year
            HAVING COUNT(*) > 1
        """).fetchall()

        for row in rows:
            add_failure(
                failures=failures,
                rule_id="DQ-04",
                severity="WARNING",
                table_name=table_name,
                record_id="",
                company_id=row[0],
                year=row[1],
                message=(
                    f"Duplicate company-year record found. "
                    f"Occurrences: {row[2]}"
                ),
            )


def validate_stock_prices(connection, failures):
    """DQ-10: Check for invalid stock closing prices."""

    rows = connection.execute("""
        SELECT
            id,
            company_id,
            date,
            close_price
        FROM stock_prices
        WHERE close_price IS NULL
           OR close_price <= 0
    """).fetchall()

    for row in rows:
        add_failure(
            failures=failures,
            rule_id="DQ-10",
            severity="CRITICAL",
            table_name="stock_prices",
            record_id=row[0],
            company_id=row[1],
            year=row[2],
            message=f"Invalid close price: {row[3]}",
        )


def write_failures(failures):
    """Write validation failures to CSV."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    columns = [
        "rule_id",
        "severity",
        "table_name",
        "record_id",
        "company_id",
        "year",
        "message",
    ]

    with open(
        FAILURES_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=columns,
        )

        writer.writeheader()
        writer.writerows(failures)


def main():

    print("=" * 70)
    print("NIFTY 100 DATA VALIDATION")
    print("=" * 70)

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    connection = sqlite3.connect(DB_PATH)

    failures = []

    print("\nRunning validation rules...")

    # DQ-01
    validate_company_count(
        connection,
        failures,
    )

    # DQ-02
    validate_duplicate_company_ids(
        connection,
        failures,
    )

    # DQ-03
    validate_foreign_keys(
        connection,
        failures,
    )

    # DQ-04
    validate_company_year_duplicates(
        connection,
        failures,
    )

    # DQ-05
    validate_positive_sales(
        connection,
        failures,
    )

    # DQ-10
    validate_stock_prices(
        connection,
        failures,
    )

    connection.close()

    write_failures(failures)

    print("\nValidation complete.")

    print(f"Total failures: {len(failures)}")

    print(f"Report: {FAILURES_FILE}")

    if failures:
        print("\nFailures found:")

        for failure in failures:
            print(
                f"  [{failure['severity']}] "
                f"{failure['rule_id']} - "
                f"{failure['table_name']} - "
                f"{failure['message']}"
            )
    else:
        print("✓ No validation failures found.")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()