from __future__ import annotations

from typing import NamedTuple


class Pair(NamedTuple):
    pair_name_id: str
    base: str
    quote: str
    spend_sum: int
    profit_markup: int
    use_stop_loss: bool
    stop_loss: int
    active: bool


class Config(NamedTuple):
    config_name_id: str

    # Список для хранения каждой пары
    pairs: dict[str, Pair]

    # Ключи для БинансАпи
    api_key: str
    api_secret: str

    klines_limits: int
    points_to_enter: int
    use_open_candles: bool
    timeframe: str
