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
print("ORPHAN RECORD COUNT")
print("=" * 70)

for file in RAW_DIR.glob("*.xlsx"):

    try:
        # Detect whether the file has a title row
        preview = pd.read_excel(file, header=None, nrows=2)

        if "Fintech" in str(preview.iloc[0, 0]):
            df = pd.read_excel(file, header=1)
        else:
            df = pd.read_excel(file, header=0)

        # Normalize column names
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("&", "and")
        )

        if "company_id" not in df.columns:
            continue

        company_ids = (
            df["company_id"]
            .dropna()
            .astype(str)
            .str.strip()
            .str.upper()
        )

        orphan_rows = df[company_ids.isin(missing_ids)]

        if len(orphan_rows) > 0:
            print(f"\n{file.name}")
            print(f"Total rows: {len(df)}")
            print(f"Orphan rows: {len(orphan_rows)}")

            print("\nBreakdown:")
            print(
                company_ids[company_ids.isin(missing_ids)]
                .value_counts()
                .sort_index()
            )

    except Exception as e:
        print(f"\nERROR: {file.name}")
        print(e)

print("\n" + "=" * 70)
print("CHECK COMPLETE")
print("=" * 70)