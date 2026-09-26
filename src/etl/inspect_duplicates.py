import sqlite3
from pathlib import Path

DB_PATH = Path("db/nifty100.db")


def show_duplicates(connection, table_name, company_id, year):
    print("\n" + "=" * 80)
    print(f"{table_name.upper()} | {company_id} | {year}")
    print("=" * 80)

    rows = connection.execute(
        f"""
        SELECT *
        FROM {table_name}
        WHERE company_id = ?
          AND year = ?
        """,
        (company_id, year),
    ).fetchall()

    columns = [
        description[0]
        for description in connection.execute(
            f"SELECT * FROM {table_name} LIMIT 0"
        ).description
    ]

    print("Columns:")
    print(columns)

    for number, row in enumerate(rows, start=1):
        print(f"\nRecord {number}:")
        for column, value in zip(columns, row):
            print(f"  {column}: {value}")


def main():
    connection = sqlite3.connect(DB_PATH)

    # Inspect a few representative duplicate cases.
    cases = [
        ("profitandloss", "ADANIPORTS", "Mar 2013"),
        ("balancesheet", "ASIANPAINT", "Mar 2013"),
        ("balancesheet", "PNB", "Mar 2013"),
        ("financial_ratios", "ABB", "Mar 2014"),
    ]

    for table_name, company_id, year in cases:
        show_duplicates(connection, table_name, company_id, year)

    connection.close()


if __name__ == "__main__":
    main()