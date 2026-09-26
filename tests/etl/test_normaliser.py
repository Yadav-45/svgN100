import pytest

from src.etl.normaliser import normalize_year, normalize_ticker


# ============================================================
# normalize_year() tests
# ============================================================

def test_year_plain_2024():
    assert normalize_year("2024") == 2024


def test_year_plain_2023():
    assert normalize_year("2023") == 2023


def test_year_fy24():
    assert normalize_year("FY24") == 2024


def test_year_fy23():
    assert normalize_year("FY23") == 2023


def test_year_fy2024():
    assert normalize_year("FY2024") == 2024


def test_year_fy2023():
    assert normalize_year("FY2023") == 2023


def test_year_range_2023_24():
    assert normalize_year("2023-24") == 2024


def test_year_range_2022_23():
    assert normalize_year("2022-23") == 2023


def test_year_range_with_slash():
    assert normalize_year("2023/24") == 2024


def test_year_lowercase_fy():
    assert normalize_year("fy24") == 2024


def test_year_with_spaces():
    assert normalize_year(" FY24 ") == 2024


def test_year_fy_with_space():
    assert normalize_year("FY 24") == 2024


def test_year_fy_full_with_space():
    assert normalize_year("FY 2024") == 2024


def test_year_range_with_spaces():
    assert normalize_year(" 2023-24 ") == 2024


def test_year_integer():
    assert normalize_year(2024) == 2024


def test_year_string_integer():
    assert normalize_year("2025") == 2025


def test_year_none():
    assert normalize_year(None) is None


def test_invalid_year_text():
    with pytest.raises(ValueError):
        normalize_year("ABC")


def test_invalid_year_short():
    with pytest.raises(ValueError):
        normalize_year("24")


def test_invalid_year_format():
    with pytest.raises(ValueError):
        normalize_year("2024XYZ")


# ============================================================
# normalize_ticker() tests
# ============================================================

def test_ticker_lowercase():
    assert normalize_ticker("reliance") == "RELIANCE"


def test_ticker_uppercase():
    assert normalize_ticker("RELIANCE") == "RELIANCE"


def test_ticker_spaces():
    assert normalize_ticker(" RELIANCE ") == "RELIANCE"


def test_ticker_internal_spaces():
    assert normalize_ticker("RELIANCE INDUSTRIES") == "RELIANCEINDUSTRIES"


def test_ticker_ns_suffix():
    assert normalize_ticker("RELIANCE.NS") == "RELIANCE"


def test_ticker_bo_suffix():
    assert normalize_ticker("RELIANCE.BO") == "RELIANCE"


def test_ticker_lowercase_ns():
    assert normalize_ticker("reliance.ns") == "RELIANCE"


def test_ticker_lowercase_bo():
    assert normalize_ticker("reliance.bo") == "RELIANCE"


def test_ticker_spaces_ns():
    assert normalize_ticker(" RELIANCE.NS ") == "RELIANCE"


def test_ticker_spaces_bo():
    assert normalize_ticker(" RELIANCE.BO ") == "RELIANCE"


def test_ticker_tcs():
    assert normalize_ticker("tcs") == "TCS"


def test_ticker_infY():
    assert normalize_ticker("infy") == "INFY"


def test_ticker_hdfc():
    assert normalize_ticker("hdfc") == "HDFC"


def test_ticker_none():
    assert normalize_ticker(None) is None


def test_ticker_numeric():
    assert normalize_ticker(123) == "123"


# ============================================================
# Additional edge-case tests
# ============================================================

def test_year_fy_with_multiple_spaces():
    assert normalize_year("FY  24") == 2024


def test_ticker_multiple_spaces():
    assert normalize_ticker("  TCS  ") == "TCS"


def test_ticker_mixed_case():
    assert normalize_ticker("ReLiAnCe") == "RELIANCE"


def test_ticker_ns_mixed_case():
    assert normalize_ticker("ReLiAnCe.Ns") == "RELIANCE"


def test_ticker_bo_mixed_case():
    assert normalize_ticker("ReLiAnCe.Bo") == "RELIANCE"