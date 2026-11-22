import allure
import pytest

from data import EMPTY_REQUIRED_FIELD_CASES, MISSING_REQUIRED_FIELD_CASES, Messages
from helpers import generate_user
from stellar_api import StellarBurgersApi


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя: успешный ответ")
    def test_create_unique_user_returns_success(self, user_data, register_user_request):
        response = register_user_request(user_data)
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 200, response.text
        assert body["success"] is True

    @allure.title("Создание уникального пользователя: возвращаются данные пользователя")
    def test_create_unique_user_returns_user_data(self, user_data, register_user_request):
        response = register_user_request(user_data)
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 200, response.text
        assert body["user"] == {"email": user_data["email"], "name": user_data["name"]}

    @allure.title("Создание уникального пользователя: возвращается Bearer accessToken")
    def test_create_unique_user_returns_access_token(self, user_data, register_user_request):
        response = register_user_request(user_data)
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 200, response.text
        assert body["accessToken"].startswith("Bearer ")

    @allure.title("Создание уникального пользователя: возвращается refreshToken")
    def test_create_unique_user_returns_refresh_token(self, user_data, register_user_request):
        response = register_user_request(user_data)
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 200, response.text
        assert body["refreshToken"]

    @allure.title("Создание пользователя, который уже зарегистрирован (те же данные)")
    def test_create_existing_user_with_same_data_error(
        self, registered_user, register_user_request
    ):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"],
        }
        response = register_user_request(payload)
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 403, response.text
        assert body == {"success": False, "message": Messages.USER_ALREADY_EXISTS}

    @allure.title("Создание пользователя, который уже зарегистрирован (тот же email, другие данные)")
    def test_create_existing_user_with_same_email_error(
        self, registered_user, register_user_request
    ):
        payload = {**generate_user(), "email": registered_user["email"]}
        response = register_user_request(payload)
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 403, response.text
        assert body == {"success": False, "message": Messages.USER_ALREADY_EXISTS}

    @allure.title("Создание пользователя — отсутствует обязательное поле: {missing_field}")
    @pytest.mark.parametrize(
        "payload, missing_field",
        MISSING_REQUIRED_FIELD_CASES,
        ids=["missing_email", "missing_password", "missing_name"],
    )
    def test_create_user_without_required_field_error(
        self, register_user_request, payload, missing_field
    ):
        response = register_user_request(payload)
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 403, response.text
        assert body == {"success": False, "message": Messages.REQUIRED_FIELDS}

    @allure.title("Создание пользователя — пустое обязательное поле: {empty_field}")
    @pytest.mark.parametrize(
        "payload, empty_field",
        EMPTY_REQUIRED_FIELD_CASES,
        ids=["empty_email", "empty_password", "empty_name"],
    )
    def test_create_user_with_empty_required_field_error(
        self, register_user_request, payload, empty_field
    ):
        response = register_user_request(payload)
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 403, response.text
        assert body == {"success": False, "message": Messages.REQUIRED_FIELDS}
