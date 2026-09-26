import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")

FILE = RAW_DIR / "1788501620089-fb3ae469-financial_ratios.xlsx"


def main():
    print("=" * 70)
    print("FINANCIAL RATIOS SOURCE CHECK")
    print("=" * 70)

    df = pd.read_excel(FILE)

    # Clean column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Find ABB records
    abb = df[
        (df["company_id"].astype(str).str.upper() == "ABB")
        & (df["year"].astype(str).isin([
            "Mar 2014",
            "Mar 2015",
            "Mar 2016",
            "Mar 2017",
            "Mar 2018",
            "Mar 2019",
            "Mar 2020",
            "Mar 2021",
            "Mar 2022",
            "Mar 2023",
            "Mar 2024",
        ]))
    ]

    print(f"\nABB records found in source: {len(abb)}")

    print("\nSource records:")
    print(abb.to_string(index=False))

    print("\n" + "=" * 70)
    print("SOURCE CHECK COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()