from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .config import BinanceConfig
from .http import HttpClient, HttpResponse


@dataclass(frozen=True)
class ServerTime:
    serverTime: int


class BinancePublicClient:
    def __init__(self, config: Optional[BinanceConfig] = None) -> None:
        cfg = config or BinanceConfig()
        self._http = HttpClient(
            base_url=cfg.base_url,
            timeout_s=cfg.timeout_s,
            retries=cfg.retries,
            backoff_base_s=cfg.backoff_base_s,
        )

    def server_time(self) -> HttpResponse:
        return self._http.get("/api/v3/time")

    def exchange_info(self, *, symbol: Optional[str] = None) -> HttpResponse:
        params = {"symbol": symbol} if symbol else None
        return self._http.get("/api/v3/exchangeInfo", params=params)

    def ticker_price(self, *, symbol: Optional[str] = None) -> HttpResponse:
        params = {"symbol": symbol} if symbol else None
        return self._http.get("/api/v3/ticker/price", params=params)

    def depth(self, *, symbol: str, limit: int = 100) -> HttpResponse:
        return self._http.get("/api/v3/depth", params={"symbol": symbol, "limit": limit})

    @staticmethod
    def parse_symbols_from_exchange_info(payload: Dict[str, Any]) -> List[str]:
        symbols = payload.get("symbols") or []
        out: List[str] = []
        for s in symbols:
            sym = s.get("symbol")
            status = s.get("status")
            if isinstance(sym, str) and status == "TRADING":
                out.append(sym)
        return out

