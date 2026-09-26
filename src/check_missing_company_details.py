from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")

missing_ids = [
    "ULTRACEMCO",
    "UNIONBANK",
    "UNITDSPR",
    "VBL",
    "VEDL",
    "WIPRO",
    "ZOMATO",
    "ZYDUSLIFE",
]

companies_file = next(RAW_DIR.glob("*companies.xlsx"))

companies = pd.read_excel(companies_file, header=1)

companies.columns = (
    companies.columns
    .astype(str)
    .str.strip()
)

print("=" * 70)
print("MISSING COMPANY MASTER DATA")
print("=" * 70)

print("\nColumns in companies.xlsx:")
print(list(companies.columns))

print("\nExisting company count:", len(companies))

print("\nChecking the 8 missing companies...")

for company_id in missing_ids:
    match = companies[
        companies["id"].astype(str).str.strip().str.upper() == company_id
    ]

    if match.empty:
        print(f"\n❌ {company_id} -> NOT PRESENT")
    else:
        print(f"\n✅ {company_id} -> FOUND")
        print(match.to_string(index=False))

print("\n" + "=" * 70)
print("CHECK COMPLETE")
print("=" * 70)