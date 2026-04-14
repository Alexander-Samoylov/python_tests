import allure
import pytest


@allure.epic("Binance: публичные API")
@allure.feature("Рыночные данные")
@allure.story("Стакан (depth)")
@allure.title("Стакан содержит bids/asks и уровни в формате [price, qty]")
@allure.description(
    "Проверяем `GET /api/v3/depth` для нескольких символов: "
    "наличие ключей `bids`/`asks`, формат уровней и что количество уровней не превышает limit."
)
@pytest.mark.parametrize("symbol,limit", [("BTCUSDT", 5), ("ETHUSDT", 10)])
def test_depth_shape(binance, symbol, limit):
    allure.dynamic.parameter("symbol", symbol)
    allure.dynamic.parameter("limit", limit)

    with allure.step(f"Отправляем запрос `GET /api/v3/depth` (symbol={symbol}, limit={limit})"):
        r = binance.depth(symbol=symbol, limit=limit)

    with allure.step("Проверяем HTTP статус и наличие ключей"):
        assert r.status_code == 200
        assert isinstance(r.json, dict)
        assert "lastUpdateId" in r.json
        assert "bids" in r.json
        assert "asks" in r.json
        assert isinstance(r.json["bids"], list)
        assert isinstance(r.json["asks"], list)

    with allure.step("Проверяем, что количество уровней не превышает limit"):
        # API обычно возвращает <= limit, не строго равно
        assert len(r.json["bids"]) <= limit
        assert len(r.json["asks"]) <= limit

    with allure.step("Проверяем формат уровней стакана"):
        for side in ("bids", "asks"):
            for level in r.json[side]:
                assert isinstance(level, list)
                assert len(level) == 2
                price, qty = level
                assert isinstance(price, str)
                assert isinstance(qty, str)

