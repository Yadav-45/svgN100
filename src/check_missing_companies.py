from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw")

missing_ids = {
    "ULTRACEMCO",
    "UNIONBANK",
    "UNITDSPR",
    "VBL",
    "VEDL",
    "WIPRO",
    "ZOMATO",
    "ZYDUSLIFE",
}


print("=" * 70)
print("CHECKING MISSING COMPANIES ACROSS ALL DATASETS")
print("=" * 70)

for file in RAW_DIR.glob("*.xlsx"):

    try:
        # Detect whether file has a title row
        preview = pd.read_excel(file, header=None, nrows=1)
        first_cell = str(preview.iloc[0, 0])

        if "Fintech" in first_cell:
            df = pd.read_excel(file, header=1)
        else:
            df = pd.read_excel(file, header=0)

        # Look for company_id or id column
        columns = [str(c).strip().lower() for c in df.columns]

        found = set()

        if "company_id" in columns:
            column = df.columns[columns.index("company_id")]
            values = set(df[column].dropna().astype(str).str.strip())
            found = missing_ids.intersection(values)

        elif "id" in columns and "companies" in file.name.lower():
            column = df.columns[columns.index("id")]
            values = set(df[column].dropna().astype(str).str.strip())
            found = missing_ids.intersection(values)

        if found:
            print(f"\n{file.name}")
            print(f"Found: {sorted(found)}")

    except Exception as e:
        print(f"\nERROR reading {file.name}: {e}")


print("\n" + "=" * 70)
print("CHECK COMPLETE")
print("=" * 70)