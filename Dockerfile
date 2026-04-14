FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
COPY tests /app/tests
COPY pytest.ini /app/pytest.ini
COPY README.md /app/README.md

RUN pip install --no-cache-dir -e .

CMD ["pytest", "-q", "--alluredir=allure-results"]

