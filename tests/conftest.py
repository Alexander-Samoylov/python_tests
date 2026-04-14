import os

import allure
import pytest

from binance_api import BinancePublicClient
from binance_api.config import BinanceConfig


@pytest.fixture(scope="session")
def binance_cfg() -> BinanceConfig:
    base_url = os.getenv("BINANCE_BASE_URL", "https://api.binance.com")
    timeout_s = float(os.getenv("BINANCE_TIMEOUT_S", "10"))
    retries = int(os.getenv("BINANCE_RETRIES", "3"))
    backoff_base_s = float(os.getenv("BINANCE_BACKOFF_BASE_S", "0.3"))
    cfg = BinanceConfig(
        base_url=base_url,
        timeout_s=timeout_s,
        retries=retries,
        backoff_base_s=backoff_base_s,
    )
    allure.dynamic.parameter("BINANCE_BASE_URL", cfg.base_url)
    allure.dynamic.parameter("BINANCE_TIMEOUT_S", cfg.timeout_s)
    allure.dynamic.parameter("BINANCE_RETRIES", cfg.retries)
    return cfg


@pytest.fixture(scope="session")
def binance(binance_cfg: BinanceConfig) -> BinancePublicClient:
    return BinancePublicClient(binance_cfg)

