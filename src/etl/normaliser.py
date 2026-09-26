import re


def normalize_year(value):
    """Convert common financial year formats into a four-digit year."""

    if value is None:
        return None

    value = str(value).strip().upper()

    # FY24 -> 2024
    match = re.fullmatch(r"FY\s*(\d{2})", value)
    if match:
        year = int(match.group(1))
        return 2000 + year

    # FY2024 -> 2024
    match = re.fullmatch(r"FY\s*(\d{4})", value)
    if match:
        return int(match.group(1))

    # 2023-24 -> 2024
    match = re.fullmatch(r"(\d{4})[-/](\d{2})", value)
    if match:
        return int(match.group(1)) + 1

    # Plain year
    if value.isdigit() and len(value) == 4:
        return int(value)

    raise ValueError(f"Invalid year format: {value}")


def normalize_ticker(value):
    """Clean and standardize a stock ticker."""

    if value is None:
        return None

    ticker = str(value).strip().upper()

    # Remove common exchange suffixes
    ticker = re.sub(r"\.(NS|BO)$", "", ticker)

    # Remove spaces
    ticker = ticker.replace(" ", "")

    return ticker