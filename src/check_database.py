import sqlite3
from pathlib import Path


DB_PATH = Path("db/nifty100.db")


def main():

    connection = sqlite3.connect(DB_PATH)

    print("=" * 70)
    print("DATABASE VALIDATION - BASIC CHECK")
    print("=" * 70)

    # TABLES
    tables = connection.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """).fetchall()

    print("\nTables:")

    for table in tables:
        print(f"  ✓ {table[0]}")

    # ROW COUNTS
    print("\nRow counts:")

    for table in tables:

        table_name = table[0]

        count = connection.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        ).fetchone()[0]

        print(f"  {table_name:<20} {count:,}")

    # COMPANY COUNT
    company_count = connection.execute(
        "SELECT COUNT(*) FROM companies"
    ).fetchone()[0]

    unique_company_count = connection.execute(
        "SELECT COUNT(DISTINCT id) FROM companies"
    ).fetchone()[0]

    print("\nCompany validation:")
    print(f"  Total companies:  {company_count}")
    print(f"  Unique companies: {unique_company_count}")

    if company_count == 100 and unique_company_count == 100:
        print("  ✓ Exactly 100 unique companies")
    else:
        print("  ❌ Company count problem")

    # FOREIGN KEY CHECK
    print("\nForeign key validation:")

    foreign_keys = connection.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()

    if len(foreign_keys) == 0:
        print("  ✓ No foreign-key violations")
    else:
        print(f"  ❌ Foreign-key violations: {len(foreign_keys)}")

        for row in foreign_keys[:10]:
            print(row)

    # DUPLICATE COMPANY IDS
    print("\nDuplicate company IDs:")

    duplicates = connection.execute("""
        SELECT id, COUNT(*) AS count
        FROM companies
        GROUP BY id
        HAVING COUNT(*) > 1
    """).fetchall()

    if len(duplicates) == 0:
        print("  ✓ No duplicate company IDs")
    else:
        print("  ❌ Duplicate IDs found:")

        for row in duplicates:
            print(row)

    # STOCK PRICE CHECK
    print("\nStock price validation:")

    invalid_prices = connection.execute("""
        SELECT COUNT(*)
        FROM stock_prices
        WHERE close_price IS NULL
           OR close_price <= 0
    """).fetchone()[0]

    if invalid_prices == 0:
        print("  ✓ No invalid closing prices")
    else:
        print(f"  ❌ Invalid closing prices: {invalid_prices}")

    # SALES CHECK
    print("\nProfit & Loss sales validation:")

    invalid_sales = connection.execute("""
        SELECT COUNT(*)
        FROM profitandloss
        WHERE sales IS NULL
           OR sales <= 0
    """).fetchone()[0]

    if invalid_sales == 0:
        print("  ✓ All sales values are positive")
    else:
        print(f"  ❌ Invalid sales values: {invalid_sales}")

    connection.close()

    print("\n" + "=" * 70)
    print("BASIC DATABASE CHECK COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()