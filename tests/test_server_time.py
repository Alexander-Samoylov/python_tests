import allure


@allure.epic("Binance: публичные API")
@allure.feature("Системные методы")
@allure.story("Время сервера")
@allure.title("Получение времени сервера возвращает корректную схему")
@allure.description(
    "Проверяем endpoint `/api/v3/time`: статус 200 и наличие поля `serverTime` (int, > 0). "
    "Используется как базовая проверка доступности API и корректности JSON."
)
def test_server_time_ok(binance):
    with allure.step("Отправляем запрос `GET /api/v3/time`"):
        r = binance.server_time()

    with allure.step("Проверяем HTTP статус"):
        assert r.status_code == 200

    with allure.step("Проверяем схему ответа"):
        assert isinstance(r.json, dict)
        assert "serverTime" in r.json
        assert isinstance(r.json["serverTime"], int)
        assert r.json["serverTime"] > 0

