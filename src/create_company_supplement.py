from pathlib import Path
import pandas as pd

OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

supplement = pd.DataFrame([
    ["ULTRACEMCO", "UltraTech Cement"],
    ["UNIONBANK", "Union Bank of India"],
    ["UNITDSPR", "United Spirits"],
    ["VBL", "Varun Beverages"],
    ["VEDL", "Vedanta"],
    ["WIPRO", "Wipro"],
    ["ZOMATO", "Zomato"],
    ["ZYDUSLIFE", "Zydus Lifesciences"],
], columns=["id", "company_name"])

output_file = OUTPUT_DIR / "company_master_supplement.csv"

supplement.to_csv(output_file, index=False)

print("=" * 60)
print("COMPANY MASTER SUPPLEMENT CREATED")
print("=" * 60)
print(f"File: {output_file}")
print(f"Companies added: {len(supplement)}")
print()
print(supplement.to_string(index=False))