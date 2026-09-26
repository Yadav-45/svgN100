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
print("MISSING COMPANY INFORMATION")
print("=" * 70)

for file in RAW_DIR.glob("*.xlsx"):

    try:
        preview = pd.read_excel(file, header=None, nrows=2)

        if "Fintech" in str(preview.iloc[0, 0]):
            df = pd.read_excel(file, header=1)
        else:
            df = pd.read_excel(file, header=0)

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

        matching = df[company_ids.isin(missing_ids)]

        if len(matching) == 0:
            continue

        print(f"\n{'=' * 70}")
        print(file.name)
        print(f"{'=' * 70}")

        print("Columns:")
        print(list(df.columns))

        print("\nSample records:")

        print(
            matching
            .head(3)
            .to_string(index=False)
        )

    except Exception as e:
        print(f"\nERROR: {file.name}")
        print(e)

print("\n" + "=" * 70)
print("EXTRACTION COMPLETE")
print("=" * 70)