import json

import allure
import requests

from data import Urls

TIMEOUT = 30
SENSITIVE_REQUEST_KEYS = {"password"}
SENSITIVE_HEADER_KEYS = {"Authorization"}
SENSITIVE_RESPONSE_KEYS = {"accessToken", "refreshToken"}


class StellarBurgersApi:

    _session = requests.Session()

    @classmethod
    def _mask_data(cls, data, sensitive_keys):
        if isinstance(data, dict):
            return {
                key: ("***" if key in sensitive_keys else cls._mask_data(value, sensitive_keys))
                for key, value in data.items()
            }
        if isinstance(data, list):
            return [cls._mask_data(item, sensitive_keys) for item in data]
        return data

    @classmethod
    def _attach_request(cls, method, url, payload=None, headers=None):
        request_info = {
            "method": method,
            "url": url,
            "headers": cls._mask_data(headers or {}, SENSITIVE_HEADER_KEYS),
            "json": cls._mask_data(payload, SENSITIVE_REQUEST_KEYS) if payload is not None else None,
        }
        allure.attach(
            json.dumps(request_info, ensure_ascii=False, indent=2),
            name=f"request [{method}]",
            attachment_type=allure.attachment_type.JSON,
        )

    @classmethod
    def _attach_response(cls, response):
        try:
            body = json.dumps(
                cls._mask_data(response.json(), SENSITIVE_RESPONSE_KEYS),
                ensure_ascii=False,
                indent=2,
            )
            attachment_type = allure.attachment_type.JSON
        except ValueError:
            body = response.text
            attachment_type = allure.attachment_type.TEXT
        allure.attach(
            body,
            name=f"response [{response.status_code}]",
            attachment_type=attachment_type,
        )

    @staticmethod
    def safe_json(response):
        try:
            return response.json()
        except ValueError:
            return None

    @classmethod
    def create_user(cls, payload):
        with allure.step("Создать пользователя: POST /api/auth/register"):
            cls._attach_request("POST", Urls.REGISTER, payload=payload)
            response = cls._session.post(Urls.REGISTER, json=payload, timeout=TIMEOUT)
            cls._attach_response(response)
            return response

    @classmethod
    def login_user(cls, payload):
        with allure.step("Авторизовать пользователя: POST /api/auth/login"):
            cls._attach_request("POST", Urls.LOGIN, payload=payload)
            response = cls._session.post(Urls.LOGIN, json=payload, timeout=TIMEOUT)
            cls._attach_response(response)
            return response

    @classmethod
    def delete_user(cls, access_token):
        headers = {"Authorization": access_token}
        with allure.step("Удалить пользователя: DELETE /api/auth/user"):
            cls._attach_request("DELETE", Urls.USER, headers=headers)
            response = cls._session.delete(Urls.USER, headers=headers, timeout=TIMEOUT)
            cls._attach_response(response)
            return response

    @classmethod
    def get_ingredients(cls):
        with allure.step("Получить список ингредиентов: GET /api/ingredients"):
            cls._attach_request("GET", Urls.INGREDIENTS)
            response = cls._session.get(Urls.INGREDIENTS, timeout=TIMEOUT)
            cls._attach_response(response)
            return response

    @classmethod
    def create_order(cls, ingredients=None, access_token=None):
        headers = {"Authorization": access_token} if access_token else {}
        payload = {"ingredients": ingredients} if ingredients is not None else {}
        with allure.step("Создать заказ: POST /api/orders"):
            cls._attach_request("POST", Urls.ORDERS, payload=payload, headers=headers)
            response = cls._session.post(
                Urls.ORDERS, json=payload, headers=headers, timeout=TIMEOUT
            )
            cls._attach_response(response)
            return response
