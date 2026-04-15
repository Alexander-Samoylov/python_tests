# Binance Public API Autotests (pet-project)

Пет‑проект автотестов для демонстрации:

- **понимания работы с крипто‑API** (публичные REST API Binance)
- **параллельности/асинхронности** (одновременные запросы к нескольким символам)
- **CI/CD** (Docker + GitLab CI)
- **отчётности** (Allure results + HTML report в CI)

## Стек

- `pytest`
- `requests`
- `allure-pytest`
- `pytest-asyncio` (для `async` тестов)
- `docker`
- `gitlab-ci`

## Что тестируем

Публичные endpoints (без API key):

- `GET /api/v3/time`
- `GET /api/v3/exchangeInfo`
- `GET /api/v3/ticker/price`
- `GET /api/v3/depth`

## Быстрый старт (локально)

Установить зависимости:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Прогон тестов:

```bash
python -m pytest -q
```

С Allure results:

```bash
python -m pytest -q --alluredir=allure-results
```

Генерация отчёта (нужен Allure CLI):

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## Линтинг (pylint)

Установить dev-зависимости:

```bash
pip install -r requirements-dev.txt
```

Проверить тесты:

```bash
python -m pylint tests/
```

## Запуск через Docker

Сборка:

```bash
docker build -t binance-autotests:local .
```

### Docker + Allure results на хосте

Чтобы забрать `allure-results` из контейнера на локальную машину, смонтируйте volume:

```bash
mkdir -p allure-results
docker run --rm \
  -v "$(pwd)/allure-results:/app/allure-results" \
  binance-autotests:local
```

### Генерация Allure HTML (2 способа)

#### Способ A — Allure CLI на хосте

```bash
allure serve allure-results
```

или статический отчёт:

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

#### Способ B — Allure CLI в Docker (без установки Allure на хост)

```bash
mkdir -p allure-report
docker run --rm \
  -v "$(pwd)/allure-results:/allure-results" \
  -v "$(pwd)/allure-report:/allure-report" \
  qameta/allure:2.29.0 \
  generate /allure-results -o /allure-report --clean
```

Откройте `allure-report/index.html` в браузере.

## CI/CD (GitLab)

В `.gitlab-ci.yml`:

- job `tests` — гоняет `pytest` и сохраняет `allure-results` как артефакт
- job `allure_report` — генерирует `allure-report` (HTML) и сохраняет как артефакт

## Структура

```text
.
├─ src/
│  └─ binance_api/
│     ├─ __init__.py
│     ├─ client.py
│     ├─ config.py
│     └─ http.py
├─ tests/
│  ├─ conftest.py
│  ├─ test_exchange_info.py
│  ├─ test_server_time.py
│  ├─ test_ticker_price_async.py
│  └─ test_orderbook_depth.py
├─ Dockerfile
├─ pytest.ini
├─ requirements.txt
└─ .gitlab-ci.yml
```

