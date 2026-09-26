import sqlite3
from pathlib import Path

DB_PATH = Path("db/nifty100.db")


def check_duplicates(connection, table_name):
    print(f"\nChecking {table_name}...")

    rows = connection.execute(f"""
        SELECT company_id, year, COUNT(*) AS record_count
        FROM {table_name}
        GROUP BY company_id, year
        HAVING COUNT(*) > 1
        ORDER BY company_id, year
    """).fetchall()

    if not rows:
        print("✓ No duplicate company/year combinations found")
        return

    print(f"⚠ Found {len(rows)} duplicate combinations")

    for row in rows[:20]:
        print(
            f"  Company: {row[0]} | "
            f"Year: {row[1]} | "
            f"Records: {row[2]}"
        )


def main():
    print("=" * 70)
    print("DUPLICATE COMPANY/YEAR VALIDATION")
    print("=" * 70)

    connection = sqlite3.connect(DB_PATH)

    for table in [
        "profitandloss",
        "balancesheet",
        "financial_ratios",
    ]:
        check_duplicates(connection, table)

    connection.close()

    print("\n" + "=" * 70)
    print("CHECK COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()