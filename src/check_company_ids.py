from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")

companies_file = next(RAW_DIR.glob("*companies.xlsx"))
pnl_file = next(RAW_DIR.glob("*profitandloss.xlsx"))

# Read companies
companies = pd.read_excel(companies_file, header=1)

# Read Profit & Loss
pnl = pd.read_excel(pnl_file, header=1)

companies.columns = companies.columns.astype(str).str.strip()
pnl.columns = pnl.columns.astype(str).str.strip()

company_ids = set(
    companies["id"].astype(str).str.strip()
)

pnl_ids = set(
    pnl["company_id"].astype(str).str.strip()
)

missing_ids = sorted(pnl_ids - company_ids)

print("=" * 60)
print("COMPANY ID CHECK")
print("=" * 60)

print(f"Companies in companies.xlsx: {len(company_ids)}")
print(f"Company IDs in Profit & Loss: {len(pnl_ids)}")
print(f"Missing company IDs: {len(missing_ids)}")

print("\nMissing IDs:")
print(missing_ids)