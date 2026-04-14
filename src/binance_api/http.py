import random
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class HttpResponse:
    status_code: int
    json: Any
    headers: Dict[str, str]


class HttpClient:
    def __init__(
        self,
        *,
        base_url: str,
        timeout_s: float,
        retries: int,
        backoff_base_s: float,
        session: Optional[requests.Session] = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout_s = timeout_s
        self._retries = retries
        self._backoff_base_s = backoff_base_s
        self._session = session or requests.Session()

    def get(self, path: str, *, params: Optional[dict] = None) -> HttpResponse:
        url = f"{self._base_url}{path}"
        last_exc: Optional[Exception] = None

        for attempt in range(self._retries + 1):
            try:
                r = self._session.get(url, params=params, timeout=self._timeout_s)
                content_type = (r.headers.get("Content-Type") or "").lower()
                if "application/json" in content_type:
                    body = r.json()
                else:
                    body = r.text
                return HttpResponse(status_code=r.status_code, json=body, headers=dict(r.headers))
            except (requests.RequestException, ValueError) as e:
                last_exc = e
                if attempt >= self._retries:
                    break
                sleep_s = self._backoff_base_s * (2**attempt) + random.uniform(0, self._backoff_base_s)
                time.sleep(sleep_s)

        assert last_exc is not None
        raise last_exc

