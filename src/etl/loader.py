from pathlib import Path
import sqlite3
import pandas as pd


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
DB_DIR = Path("db")

DB_PATH = DB_DIR / "nifty100.db"
SCHEMA_PATH = DB_DIR / "schema.sql"
SUPPLEMENT_FILE = PROCESSED_DIR / "company_master_supplement.csv"


def read_excel_file(file_path):
    """Read an Excel file and automatically detect the header row."""

    preview = pd.read_excel(file_path, header=None, nrows=3)

    first_cell = str(preview.iloc[0, 0])

    if "Fintech" in first_cell:
        df = pd.read_excel(file_path, header=1)
    else:
        df = pd.read_excel(file_path, header=0)

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("&", "and")
    )

    return df


def create_database():
    """Create SQLite database and apply schema."""

    DB_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    connection.execute("PRAGMA foreign_keys = ON")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    connection.executescript(schema)

    return connection


def load_companies(connection):
    """Load 92 original companies + 8 supplementary companies."""

    print("\n" + "=" * 60)
    print("LOADING COMPANY MASTER")
    print("=" * 60)

    companies_file = RAW_DIR / "1788501606103-7177b6c2-companies.xlsx"

    companies = read_excel_file(companies_file)

    print(f"Original companies: {len(companies)}")

    # Load supplementary company master
    if not SUPPLEMENT_FILE.exists():
        raise FileNotFoundError(
            f"Supplement file not found: {SUPPLEMENT_FILE}"
        )

    supplement = pd.read_csv(SUPPLEMENT_FILE)

    print(f"Supplementary companies: {len(supplement)}")

    # Add missing columns so both datasets have same structure
    for column in companies.columns:
        if column not in supplement.columns:
            supplement[column] = None

    # Keep the same column order
    supplement = supplement[companies.columns]

    # Combine
    companies = pd.concat(
        [companies, supplement],
        ignore_index=True
    )

    # Normalize IDs
    companies["id"] = (
        companies["id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # Check duplicate IDs
    duplicate_ids = companies[
        companies["id"].duplicated(keep=False)
    ]["id"].unique()

    if len(duplicate_ids) > 0:
        raise ValueError(
            f"Duplicate company IDs found: {list(duplicate_ids)}"
        )

    print(f"Final company master: {len(companies)}")

    if len(companies) != 100:
        raise ValueError(
            f"Expected 100 companies, found {len(companies)}"
        )

    companies.to_sql(
        "companies",
        connection,
        if_exists="append",
        index=False
    )

    print("✓ Company master loaded successfully")
    print("✓ 100 unique companies verified")


def load_file(connection, filename, table_name):
    file_path = RAW_DIR / filename

    if not file_path.exists():
        print(f"WARNING: File not found: {filename}")
        return

    print(f"\nLoading: {filename}")

    df = read_excel_file(file_path)

    print(f"Rows read: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    df = df.dropna(how="all")

    if table_name in {
        "profitandloss",
        "balancesheet",
        "financial_ratios",
    }:
        before = len(df)

        comparison_columns = [
            column
            for column in df.columns
            if column != "id"
        ]

        df = df.drop_duplicates(
            subset=comparison_columns,
            keep="first"
        )

        duplicates_removed = before - len(df)

        if duplicates_removed:
            print(
                f"Exact duplicate rows removed: "
                f"{duplicates_removed}"
            )

    df.to_sql(
        table_name,
        connection,
        if_exists="append",
        index=False
    )

    print(f"✓ Loaded {len(df)} rows into {table_name}")

def main():

    print("=" * 60)
    print("NIFTY 100 ETL LOADER")
    print("=" * 60)

    connection = create_database()

    try:

        # --------------------------------------------------
        # 1. COMPANY MASTER
        # --------------------------------------------------

        load_companies(connection)

        # --------------------------------------------------
        # 2. FINANCIAL / SUPPORTING DATA
        # --------------------------------------------------

        datasets = {

            "profitandloss":
                "1788501607124-aad40f4f-profitandloss.xlsx",

            "balancesheet":
                "1788501604829-ac8c0874-balancesheet.xlsx",

            "analysis":
                "1788501604303-57986a9b-analysis.xlsx",

            "documents":
                "1788501606362-ba899c04-documents.xlsx",

            "prosandcons":
                "1788501607452-d6bbe55b-prosandcons.xlsx",

            "financial_ratios":
                "1788501620089-fb3ae469-financial_ratios.xlsx",

            "market_cap":
                "1788501620397-69ae3e7f-market_cap.xlsx",

            "peer_groups":
                "1788501620796-5060f580-peer_groups.xlsx",

            "sectors":
                "1788501621129-8684701e-sectors.xlsx",

            "stock_prices":
                "1788501621395-a51977cd-stock_prices.xlsx",
        }

        for table_name, filename in datasets.items():
            load_file(
                connection,
                filename,
                table_name
            )

        connection.commit()

        print("\n" + "=" * 60)
        print("ETL LOADING COMPLETE")
        print("=" * 60)

    except Exception as error:

        connection.rollback()

        print("\n" + "=" * 60)
        print("ETL FAILED")
        print("=" * 60)

        print(f"Error: {error}")

        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()