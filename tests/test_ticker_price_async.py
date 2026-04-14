import asyncio

import allure
import pytest


async def _ticker_price_async(binance, symbol: str):
    # requests блокирующий; демонстрируем "async" конкурентность, выполняя вызов в отдельном потоке.
    return await asyncio.to_thread(binance.ticker_price, symbol=symbol)


@allure.epic("Binance: публичные API")
@allure.feature("Рыночные данные")
@allure.story("Тикер цены (параллельные запросы)")
@allure.title("Параллельный fan-out запросов цен по нескольким символам (asyncio + threads)")
@allure.description(
    "Демонстрация асинхронности: делаем несколько запросов `GET /api/v3/ticker/price` параллельно через "
    "`asyncio.gather`, используя `asyncio.to_thread` для выполнения блокирующего `requests` в пуле потоков. "
    "Проверяем статус 200 и базовую схему ответа для каждого символа."
)
@pytest.mark.asyncio
async def test_ticker_price_parallel(binance):
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
    allure.dynamic.parameter("symbols", ", ".join(symbols))

    with allure.step("Формируем задачи для параллельного выполнения запросов"):
        tasks = [_ticker_price_async(binance, s) for s in symbols]

    with allure.step("Выполняем запросы параллельно (asyncio.gather)"):
        results = await asyncio.gather(*tasks)

    for symbol, r in zip(symbols, results, strict=True):
        with allure.step(f"Проверяем ответ для {symbol}"):
            assert r.status_code == 200
            assert isinstance(r.json, dict)
            assert r.json.get("symbol") == symbol
            assert "price" in r.json
            assert isinstance(r.json["price"], str)
            assert float(r.json["price"]) > 0.0

