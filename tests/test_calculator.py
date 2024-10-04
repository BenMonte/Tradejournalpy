import math
import sys
import os
from datetime import date

# Allow imports from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models import Trade, PerformanceSummary
from calculator import calculate


def _trade(d: str, pnl: float, ret: float, r: float) -> Trade:
    return Trade(date.fromisoformat(d), pnl, ret, r)


def _mixed_trades() -> list[Trade]:
    """3 winners, 7 losers — same fixture as the Java tests."""
    return [
        _trade("2024-01-02", -100, -1.0, -1.0),
        _trade("2024-01-03",  -80, -0.8, -0.8),
        _trade("2024-01-04", -120, -1.2, -1.2),
        _trade("2024-01-05",  500,  5.0,  5.0),
        _trade("2024-01-08",  -90, -0.9, -0.9),
        _trade("2024-01-09", -110, -1.1, -1.1),
        _trade("2024-01-10", -100, -1.0, -1.0),
        _trade("2024-01-11",  300,  3.0,  3.0),
        _trade("2024-01-12",  -95, -0.95, -0.95),
        _trade("2024-01-15",  400,  4.0,  4.0),
    ]


# --- Tests ---

def test_empty_trade_list():
    s = calculate([], 10_000)
    assert s.total_trades == 0
    assert s.win_rate == 0.0
    assert s.max_drawdown_percent == 0.0


def test_single_winning_trade():
    trades = [_trade("2024-01-02", 200, 2.0, 2.0)]
    s = calculate(trades, 10_000)
    assert s.total_trades == 1
    assert s.win_rate == 1.0
    assert math.isclose(s.expectancy_r, 2.0, abs_tol=1e-9)
    assert s.max_drawdown_percent == 0.0
    assert s.max_consecutive_losses == 0


def test_win_rate():
    s = calculate(_mixed_trades(), 10_000)
    assert math.isclose(s.win_rate, 0.3, abs_tol=1e-9)


def test_expectancy_r():
    s = calculate(_mixed_trades(), 10_000)
    assert math.isclose(s.expectancy_r, 0.505, abs_tol=0.001)


def test_profit_factor():
    s = calculate(_mixed_trades(), 10_000)
    assert math.isclose(s.profit_factor, 12.0 / 6.95, abs_tol=1e-9)


def test_profit_factor_all_winners():
    trades = [
        _trade("2024-01-02", 100, 1.0, 1.0),
        _trade("2024-01-03", 200, 2.0, 2.0),
    ]
    s = calculate(trades, 10_000)
    assert s.profit_factor == float("inf")


def test_max_consecutive_losses():
    s = calculate(_mixed_trades(), 10_000)
    assert s.max_consecutive_losses == 3


def test_max_drawdown_percent():
    s = calculate(_mixed_trades(), 10_000)
    assert math.isclose(s.max_drawdown_percent, 0.03, abs_tol=1e-9)


def test_average_r():
    s = calculate(_mixed_trades(), 10_000)
    assert math.isclose(s.average_r, 0.505, abs_tol=1e-9)


def test_std_dev_r():
    s = calculate(_mixed_trades(), 10_000)
    rs = [-1.0, -0.8, -1.2, 5.0, -0.9, -1.1, -1.0, 3.0, -0.95, 4.0]
    mean = 0.505
    sum_sq = sum((r - mean) ** 2 for r in rs)
    expected = math.sqrt(sum_sq / 9)
    assert math.isclose(s.std_dev_r, expected, abs_tol=1e-9)


def test_largest_win_and_loss():
    s = calculate(_mixed_trades(), 10_000)
    assert math.isclose(s.largest_win_r, 5.0, abs_tol=1e-9)
    assert math.isclose(s.largest_loss_r, -1.2, abs_tol=1e-9)
