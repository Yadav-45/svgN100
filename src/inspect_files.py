from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw")
SUPPORTING_DIR = Path("data/supporting")


def inspect_folder(folder):
    print("\n" + "=" * 60)
    print(f"FOLDER: {folder}")
    print("=" * 60)

    if not folder.exists():
        print("Folder does not exist.")
        return

    files = list(folder.glob("*.xlsx"))

    if not files:
        print("No Excel files found.")
        return

    for file in files:
        print("\n" + "-" * 60)
        print(f"FILE: {file.name}")
        print("-" * 60)

        try:
            excel = pd.ExcelFile(file)

            print("Sheets:")
            for sheet in excel.sheet_names:
                print(f"  - {sheet}")

                df = pd.read_excel(file, sheet_name=sheet)

                print(f"Rows: {len(df)}")
                print(f"Columns: {len(df.columns)}")
                print("Column names:")
                print(list(df.columns))

        except Exception as e:
            print(f"ERROR: {e}")


inspect_folder(RAW_DIR)
inspect_folder(SUPPORTING_DIR)