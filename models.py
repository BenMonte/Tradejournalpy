from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Trade:
    entry_date: date
    trade_pnl: float
    trade_return_percent: float
    r_multiple: float


@dataclass(frozen=True)
class PerformanceSummary:
    total_trades: int
    win_rate: float
    expectancy_r: float
    average_r: float
    average_win_r: float
    average_loss_r: float
    profit_factor: float
    largest_win_r: float
    largest_loss_r: float
    std_dev_r: float
    max_consecutive_losses: int
    max_drawdown_percent: float
