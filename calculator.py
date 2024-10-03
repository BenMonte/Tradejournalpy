import math
from statistics import stdev
from models import PerformanceSummary, Trade


def calculate(trades: list[Trade], initial_capital: float = 10_000) -> PerformanceSummary:
    if not trades:
        return PerformanceSummary(
            total_trades=0, win_rate=0, expectancy_r=0, average_r=0,
            average_win_r=0, average_loss_r=0, profit_factor=0,
            largest_win_r=0, largest_loss_r=0, std_dev_r=0,
            max_consecutive_losses=0, max_drawdown_percent=0,
        )

    total = len(trades)
    winners = [t for t in trades if t.trade_pnl > 0]
    losers = [t for t in trades if t.trade_pnl <= 0]

    win_rate = len(winners) / total
    loss_rate = len(losers) / total

    rs = [t.r_multiple for t in trades]
    average_r = sum(rs) / total

    average_win_r = sum(t.r_multiple for t in winners) / len(winners) if winners else 0.0
    average_loss_r = sum(t.r_multiple for t in losers) / len(losers) if losers else 0.0

    expectancy_r = win_rate * average_win_r - loss_rate * abs(average_loss_r)

    gross_win_r = sum(t.r_multiple for t in winners)
    gross_loss_r = sum(abs(t.r_multiple) for t in losers)
    if gross_loss_r == 0:
        profit_factor = float("inf") if gross_win_r > 0 else 0.0
    else:
        profit_factor = gross_win_r / gross_loss_r

    largest_win_r = max(rs)
    largest_loss_r = min(rs)

    std_dev_r = stdev(rs) if len(rs) >= 2 else 0.0

    max_consec = _max_consecutive_losses(trades)
    max_dd = _max_drawdown(trades, initial_capital)

    return PerformanceSummary(
        total_trades=total,
        win_rate=win_rate,
        expectancy_r=expectancy_r,
        average_r=average_r,
        average_win_r=average_win_r,
        average_loss_r=average_loss_r,
        profit_factor=profit_factor,
        largest_win_r=largest_win_r,
        largest_loss_r=largest_loss_r,
        std_dev_r=std_dev_r,
        max_consecutive_losses=max_consec,
        max_drawdown_percent=max_dd,
    )


def _max_consecutive_losses(trades: list[Trade]) -> int:
    best = 0
    current = 0
    for t in trades:
        if t.trade_pnl <= 0:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def _max_drawdown(trades: list[Trade], initial_capital: float) -> float:
    peak = initial_capital
    equity = initial_capital
    worst = 0.0
    for t in trades:
        equity += t.trade_pnl
        if equity > peak:
            peak = equity
        dd = (peak - equity) / peak
        if dd > worst:
            worst = dd
    return worst
