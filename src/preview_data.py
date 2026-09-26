from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")

for file in RAW_DIR.glob("*.xlsx"):

    print("\n" + "=" * 80)
    print(f"FILE: {file.name}")
    print("=" * 80)

    try:
        excel = pd.ExcelFile(file)
        sheet = excel.sheet_names[0]

        df = pd.read_excel(
            file,
            sheet_name=sheet,
            header=None,
            nrows=5
        )

        print(df.to_string(index=False, header=False))

    except Exception as e:
        print(f"ERROR: {e}")