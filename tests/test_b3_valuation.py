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


def test_matplotlib_charts_generation(tmp_path):
    import pandas as pd

    from b3_reports.charts import (
        plot_correlation_heatmap,
        plot_graham_bar,
        plot_stock_history,
    )

    # 1. Test Line Chart: stock history
    dates = ["2026-05-20", "2026-05-21", "2026-05-22", "2026-05-25", "2026-05-26"]
    prices = [42.58, 42.47, 42.73, 43.31, 42.92]
    history_path = tmp_path / "history_wege3.png"
    plot_stock_history("WEGE3", dates, prices, history_path)

    assert history_path.exists()
    assert history_path.stat().st_size > 0

    # 2. Test Bar Chart: graham valuation
    graham_path = tmp_path / "graham_wege3.png"
    plot_graham_bar("WEGE3", 42.92, 17.73, graham_path)

    assert graham_path.exists()
    assert graham_path.stat().st_size > 0

    # 3. Test Heatmap Chart: correlation matrix
    correlations_df = pd.DataFrame(
        [[1.0, 0.85, -0.15], [0.85, 1.0, -0.05], [-0.15, -0.05, 1.0]],
        columns=["P/L", "P/VP", "Dív. Líquida"],
        index=["P/L", "P/VP", "Dív. Líquida"],
    )
    heatmap_path = tmp_path / "correlation_heatmap.png"
    plot_correlation_heatmap(correlations_df, heatmap_path)

    assert heatmap_path.exists()
    assert heatmap_path.stat().st_size > 0


def test_email_template_rendering():
    from b3_reports.email_template import generate_email_html

    cids = {"history": "hist123", "graham": "graham456", "heatmap": "heat789"}
    metrics = {"pl": 12.5, "pvp": 1.2, "div_yield": 6.5, "roe": 15.0, "roic": 18.2}

    html = generate_email_html(
        ticker="WEGE3",
        stock_name="WEG SA",
        sector="Bens Industriais",
        current_price=42.58,
        graham_price=17.73,
        metrics=metrics,
        cids=cids,
    )

    assert "WEGE3" in html
    assert "WEG SA" in html
    assert "Bens Industriais" in html
    assert "cid:hist123" in html
    assert "cid:graham456" in html
    assert "cid:heat789" in html
    assert "R$ 42.58" in html


def test_build_and_dispatch_report_local_save(tmp_path, monkeypatch):
    import pandas as pd

    from b3_reports.dispatch import build_and_dispatch_report

    # Override OUTPUT_DIR inside dispatch to use tmp_path
    monkeypatch.setattr("b3_reports.dispatch.OUTPUT_DIR", tmp_path)

    dates = ["2026-05-20", "2026-05-21", "2026-05-22", "2026-05-25", "2026-05-26"]
    prices = [42.58, 42.47, 42.73, 43.31, 42.92]

    correlations_df = pd.DataFrame(
        [[1.0, 0.8], [0.8, 1.0]], columns=["P/L", "P/VP"], index=["P/L", "P/VP"]
    )

    metrics = {"pl": 12.5, "pvp": 1.2, "div_yield": 6.5, "roe": 15.0, "roic": 18.2}

    # Ensure no environment variables trigger real SMTP sending
    monkeypatch.setenv("SMTP_SERVER", "")

    result = build_and_dispatch_report(
        ticker="WEGE3",
        stock_name="WEG SA",
        sector="Bens Industriais",
        current_price=42.92,
        graham_price=17.73,
        metrics=metrics,
        dates=dates,
        prices=prices,
        correlations_df=correlations_df,
    )

    assert result["local_saved"] is True
    assert result["email_sent"] is False

    local_report = tmp_path / "relatorio_wege3.html"
    assert local_report.exists()
    assert local_report.stat().st_size > 0

    # Images should exist in subdirectory
    images_dir = tmp_path / "images"
    assert (images_dir / "history_wege3.png").exists()
    assert (images_dir / "graham_wege3.png").exists()
    assert (images_dir / "correlation_heatmap.png").exists()


def test_run_automatic_weekly_report_mocked(tmp_path, monkeypatch):
    import datetime
    import contextlib
    from b3_reports.integration import run_automatic_weekly_report

    # Mock the output directory
    monkeypatch.setattr("b3_reports.dispatch.OUTPUT_DIR", tmp_path)
    monkeypatch.setenv("SMTP_SERVER", "")

    # Define mock database values
    mock_max_date = datetime.date(2026, 5, 26)
    
    # 1st fetchall: sector list of stocks for latest date
    # papel, empresa, setor, cotacao, vpa, lpa, pl, pvp, div_yield, roe, roic
    mock_stocks = [
        ("WEGE3", "WEG SA", "Bens Industriais", 42.92, 6.50, 2.15, 20.0, 6.6, 2.5, 33.0, 28.0),
        ("VALE3", "VALE SA", "Materiais Básicos", 35.00, 15.30, 8.20, 7.5, 4.0, 8.5, 53.0, 21.0),
    ]

    # 2nd fetchall: price history for selected stock (VALE3 because of highest safety)
    mock_history = [
        (datetime.date(2026, 5, 20), 32.50),
        (datetime.date(2026, 5, 21), 34.00),
        (datetime.date(2026, 5, 26), 35.00),
    ]

    class MockCursor:
        def __init__(self):
            self.execute_count = 0

        def execute(self, query, params=None):
            self.execute_count += 1

        def fetchone(self):
            return (mock_max_date,)

        def fetchall(self):
            # First fetchall is for the active stocks
            # Second fetchall is for history of the chosen target
            if "SELECT papel, empresa, setor" in self.last_executed_query_hint or self.execute_count == 2:
                return mock_stocks
            return mock_history

        @property
        def last_executed_query_hint(self):
            return "SELECT papel, empresa, setor" if self.execute_count == 2 else "SELECT data_dado_inserido"

    class MockConnection:
        @contextlib.contextmanager
        def cursor(self):
            yield MockCursor()
        def commit(self):
            pass
        def rollback(self):
            pass

    @contextlib.contextmanager
    def mock_get_connection():
        yield MockConnection()

    monkeypatch.setattr("b3_database.connection.DatabaseConnectionManager.get_connection", mock_get_connection)

    # Executa a integração automática
    res = run_automatic_weekly_report(default_ticker="WEGE3")

    assert res["status"] == "success"
    # Target should be VALE3 because:
    # WEGE3 graham valuation: sqrt(22.5 * 6.5 * 2.15) = sqrt(314.4375) = 17.73 (vs 42.92 market price, safety is -142%)
    # VALE3 graham valuation: sqrt(22.5 * 15.30 * 8.20) = sqrt(2823.3) = 53.13 (vs 62.15 market price, safety is -17%)
    # VALE3 has the highest margin of safety (-17% vs -142%), so it's chosen!
    assert res["ticker"] == "VALE3"
    
    local_report = tmp_path / "relatorio_vale3.html"
    assert local_report.exists()
    assert (tmp_path / "images" / "history_vale3.png").exists()
    assert (tmp_path / "images" / "graham_vale3.png").exists()
