from dataclasses import dataclass


@dataclass(frozen=True)
class BinanceConfig:
    base_url: str = "https://api.binance.com"
    timeout_s: float = 10.0
    retries: int = 3
    backoff_base_s: float = 0.3

