from pathlib import Path
import pandas as pd

OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

missing_companies = [
    "ULTRACEMCO",
    "UNIONBANK",
    "UNITDSPR",
    "VBL",
    "VEDL",
    "WIPRO",
    "ZOMATO",
    "ZYDUSLIFE",
]

df = pd.DataFrame({
    "company_id": missing_companies,
    "status": "missing_from_company_master",
    "action": "requires_master_data"
})

output_file = OUTPUT_DIR / "missing_companies.csv"

df.to_csv(output_file, index=False)

print("=" * 60)
print("MISSING COMPANY LIST CREATED")
print("=" * 60)
print(f"File: {output_file}")
print(f"Companies: {len(df)}")
print()
print(df.to_string(index=False))