import sqlite3
from pathlib import Path

DB_PATH = Path("db/nifty100.db")


def classify_table(connection, table_name):
    print("\n" + "=" * 70)
    print(f"TABLE: {table_name}")
    print("=" * 70)

    duplicate_groups = connection.execute(
        f"""
        SELECT company_id, year, COUNT(*) AS record_count
        FROM {table_name}
        GROUP BY company_id, year
        HAVING COUNT(*) > 1
        """
    ).fetchall()

    exact_duplicate_rows = 0
    conflicting_groups = 0

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

        # Remove the ID column before comparing records.
        values = [row[1:] for row in rows]

        if all(row == values[0] for row in values):
            exact_duplicate_rows += record_count - 1
        else:
            conflicting_groups += 1

            print(
                f"⚠ CONFLICT: {company_id} | "
                f"{year} | {record_count} records"
            )

    print(f"\nDuplicate groups: {len(duplicate_groups)}")
    print(f"Exact duplicate rows: {exact_duplicate_rows}")
    print(f"Conflicting groups: {conflicting_groups}")


def main():
    connection = sqlite3.connect(DB_PATH)

    for table_name in [
        "profitandloss",
        "balancesheet",
        "financial_ratios",
    ]:
        classify_table(connection, table_name)

    connection.close()

    print("\n" + "=" * 70)
    print("DUPLICATE CLASSIFICATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()