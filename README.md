# Stellar Burgers — тесты API

Автотесты ручек [Stellar Burgers](https://stellarburgers.education-services.ru/): `pytest` + `requests` + `allure-pytest`

## Что проверяется

| Файл | Ручка |
|---|---|
| `tests/test_create_user.py` | `POST /api/auth/register` |
| `tests/test_login_user.py` | `POST /api/auth/login` |
| `tests/test_create_order.py` | `POST /api/orders` |

## Структура

- `data.py` — URL, тексты ответов, тестовые константы
- `helpers.py` — генерация данных
- `stellar_api.py` — запросы к API
- `conftest.py` — фикстуры 
- `allure_results/` — результаты прогона для Allure

## Запуск

```bash
pip install -r requirements.txt
pytest
```

## Отчёт Allure

```bash
allure serve allure_results
```