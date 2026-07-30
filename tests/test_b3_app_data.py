import pandas as pd
from b3_app.data import METRIC_HELPS
from b3_app.stock import (
    check_stock_data_integrity,
    get_stock_data_val,
    normalize_price_value,
    format_thousands,
)


def test_metric_helps_completeness():
    assert "pl" in METRIC_HELPS
    assert "pvp" in METRIC_HELPS
    assert "vpa" in METRIC_HELPS
    assert "lpa" in METRIC_HELPS


def test_normalize_price_value():
    assert normalize_price_value("R$ 42,58") == 42.58
    assert normalize_price_value("10,5") == 10.5
    assert normalize_price_value(None) is None
    assert normalize_price_value("invalid") is None


def test_format_thousands():
    assert format_thousands(4197317984) == "4.197.317.984"
    assert format_thousands("1000") == "1.000"
    assert format_thousands(None) == "N/A"


def test_get_stock_data_val_dataframe():
    data = {
        "papel": ["PETR4", "VALE3"],
        "cotacao": [38.50, 62.10],
        "pl": [4.2, 7.5],
    }
    df = pd.DataFrame(data)

    assert get_stock_data_val(df, "PETR4", "cotacao") == 38.50
    assert get_stock_data_val(df, "VALE3", "pl") == 7.5
    assert get_stock_data_val(df, "WEGE3", "cotacao") is None
    assert get_stock_data_val(df, "PETR4", "coluna_inexistente") is None


def test_check_stock_data_integrity():
    integrity = check_stock_data_integrity("WEGE3")
    assert isinstance(integrity, dict)
    assert "Preços Históricos" in integrity
    assert "Histórico Mensal" in integrity
