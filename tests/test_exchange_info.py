"""Tests for Binance `/api/v3/exchangeInfo` public endpoint."""

import allure


@allure.epic("Binance: публичные API")
@allure.feature("Рыночные данные")
@allure.story("Справочник биржи (exchangeInfo)")
@allure.title("exchangeInfo содержит список торговых инструментов")
@allure.description(
    "Проверяем `GET /api/v3/exchangeInfo`: статус 200 и наличие массива `symbols`."
)
def test_exchange_info_has_symbols(binance):
    with allure.step("Отправляем запрос `GET /api/v3/exchangeInfo`"):
        r = binance.exchange_info()

    with allure.step("Проверяем HTTP статус и базовую схему"):
        assert r.status_code == 200
        assert isinstance(r.json, dict)
        assert "symbols" in r.json
        assert isinstance(r.json["symbols"], list)
        assert len(r.json["symbols"]) > 0


@allure.epic("Binance: публичные API")
@allure.feature("Рыночные данные")
@allure.story("Справочник биржи (exchangeInfo)")
@allure.title("Из exchangeInfo можно извлечь TRADING-символы (включая BTCUSDT)")
@allure.description(
    "Проверяем, что из `exchangeInfo` извлекаются символы со статусом `TRADING` "
    "и что среди них присутствует `BTCUSDT` как стабильная контрольная пара."
)
def test_exchange_info_trading_symbols_extractable(binance):
    with allure.step("Отправляем запрос `GET /api/v3/exchangeInfo`"):
        r = binance.exchange_info()

    with allure.step("Проверяем HTTP статус"):
        assert r.status_code == 200

    with allure.step("Извлекаем список символов со статусом TRADING"):
        trading = binance.parse_symbols_from_exchange_info(r.json)

    with allure.step("Проверяем, что контрольная пара BTCUSDT торгуется"):
        assert isinstance(trading, list)
        assert "BTCUSDT" in trading
