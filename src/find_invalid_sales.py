import sqlite3
from pathlib import Path

DB_PATH = Path("db/nifty100.db")

connection = sqlite3.connect(DB_PATH)

rows = connection.execute("""
    SELECT
        id,
        company_id,
        year,
        sales,
        expenses,
        operating_profit,
        net_profit,
        eps
    FROM profitandloss
    WHERE sales IS NULL
       OR sales <= 0
""").fetchall()

print("=" * 70)
print("INVALID SALES RECORDS")
print("=" * 70)

print(f"\nInvalid records found: {len(rows)}")

for row in rows:
    print("\nID:", row[0])
    print("Company:", row[1])
    print("Year:", row[2])
    print("Sales:", row[3])
    print("Expenses:", row[4])
    print("Operating Profit:", row[5])
    print("Net Profit:", row[6])
    print("EPS:", row[7])

connection.close()

print("\n" + "=" * 70)
print("CHECK COMPLETE")
print("=" * 70)