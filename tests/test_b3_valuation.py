import math

from b3_models.stock import B3StockData


def test_pydantic_finance_float_parsing():
    # Test valid floats with Brazilian/Percent formats
    assert B3StockData.parse_finance_float("1.250.342,50%") == 1250342.50
    assert B3StockData.parse_finance_float("1.250,55") == 1250.55
    assert B3StockData.parse_finance_float("-12,45%") == -12.45
    assert B3StockData.parse_finance_float("  0,00  ") == 0.0

    # Test empty or invalid formats
    assert B3StockData.parse_finance_float(None) == 0.0
    assert B3StockData.parse_finance_float("") == 0.0
    assert B3StockData.parse_finance_float("N/A") == 0.0


def test_pydantic_shares_parsing():
    # Test normal numbers with dot separator
    assert B3StockData.parse_shares("415.000.000") == 415000000
    assert B3StockData.parse_shares("10.500") == 10500

    # Test fallback
    assert B3StockData.parse_shares(None) == 0
    assert B3StockData.parse_shares("") == 0
    assert B3StockData.parse_shares("invalid") == 0


def test_pydantic_stock_creation():
    raw_data = {
        "papel": "WEGE3",
        "tipo": "ON",
        "empresa": "WEG SA",
        "setor": "Bens Industriais",
        "cotacao": "42,58",
        "dt_ult_cotacao": "26/05/2026",
        "vpa": "6,50",
        "lpa": "2,15",
        "nr_acoes": "4.197.317.984",
    }

    stock = B3StockData(**raw_data)
    assert stock.papel == "WEGE3"
    assert stock.tipo == "ON"
    assert stock.cotacao == 42.58
    assert stock.vpa == 6.50
    assert stock.lpa == 2.15
    assert stock.nr_acoes == 4197317984
    assert stock.min_52_sem == 0.0  # default value


def test_graham_formula_math():
    # Graham Intrinsic Value formula: sqrt(Constant * VPA * LPA)
    graham_constant = 22.5
    vpa_f = 2.0
    lpa_f = 5.0

    # Math logic: 22.5 * 2 * 5 = 225. sqrt(225) = 15.0
    valor_gh = round(graham_constant * vpa_f * lpa_f, 2)
    valor_jt = round(math.sqrt(valor_gh), 2)

    assert valor_gh == 225.0
    assert valor_jt == 15.0

    # With non-perfect square
    # 22.5 * 6.5 * 2.15 = 314.4375. sqrt(314.4375) = 17.7323... -> 17.73
    vpa_f2 = 6.50
    lpa_f2 = 2.15
    valor_gh2 = round(graham_constant * vpa_f2 * lpa_f2, 2)
    valor_jt2 = round(math.sqrt(valor_gh2), 2)

    assert valor_gh2 == 314.44
    assert valor_jt2 == 17.73
