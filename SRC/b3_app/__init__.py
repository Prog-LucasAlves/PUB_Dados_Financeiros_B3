"""App support package for PUB Dados Financeiros B3."""

from .data import (
    METRIC_HELPS,
    load_b3_data,
    load_market_index_data,
    load_parquet_data,
    load_stock_prices,
)
from .theme import inject_custom_css, render_status_card
from .ui import (
    apply_plotly_theme,
    fmt_decimal,
    fmt_money,
    fmt_percent,
    render_market_index,
    render_metric_card,
)
from .stock import (
    check_stock_data_integrity,
    format_thousands,
    get_stock_data_val,
    load_accumulated_return,
    load_price_history,
    normalize_price_value,
    prepare_price_metrics,
    try_load_stock_prices,
)

__all__ = [
    "METRIC_HELPS",
    "load_b3_data",
    "load_market_index_data",
    "load_parquet_data",
    "load_stock_prices",
    "inject_custom_css",
    "render_status_card",
    "apply_plotly_theme",
    "fmt_decimal",
    "fmt_money",
    "fmt_percent",
    "render_market_index",
    "render_metric_card",
    "check_stock_data_integrity",
    "estimate_accumulated_return",
    "format_thousands",
    "get_stock_data_val",
    "load_accumulated_return",
    "load_price_history",
    "normalize_price_value",
    "prepare_price_metrics",
    "try_load_stock_prices",
]
