import re
from pathlib import Path

from b3_app import METRIC_HELPS


def test_app_metric_help_keys_are_defined():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    source = app_path.read_text(encoding="utf-8")

    referenced_keys = re.findall(r'METRIC_HELPS\["([^"]+)"\]', source)
    missing_keys = [key for key in referenced_keys if key not in METRIC_HELPS]

    assert not missing_keys, f"Metric help entries missing: {missing_keys}"
