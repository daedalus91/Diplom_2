import allure

from data import Messages
from stellar_api import StellarBurgersApi


@allure.feature("Логин пользователя")
class TestLoginUser:

    @allure.title("Вход под существующим пользователем: успешный ответ")
    def test_login_existing_user_returns_success(self, registered_user):
        response = StellarBurgersApi.login_user(
            {"email": registered_user["email"], "password": registered_user["password"]}
        )
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 200, response.text
        assert body["success"] is True

    @allure.title("Вход под существующим пользователем: возвращаются данные пользователя")
    def test_login_existing_user_returns_user_data(self, registered_user):
        response = StellarBurgersApi.login_user(
            {"email": registered_user["email"], "password": registered_user["password"]}
        )
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 200, response.text
        assert body["user"] == {"email": registered_user["email"], "name": registered_user["name"]}

    @allure.title("Вход под существующим пользователем: возвращается Bearer accessToken")
    def test_login_existing_user_returns_access_token(self, registered_user):
        response = StellarBurgersApi.login_user(
            {"email": registered_user["email"], "password": registered_user["password"]}
        )
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 200, response.text
        assert body["accessToken"].startswith("Bearer ")

    @allure.title("Вход под существующим пользователем: возвращается refreshToken")
    def test_login_existing_user_returns_refresh_token(self, registered_user):
        response = StellarBurgersApi.login_user(
            {"email": registered_user["email"], "password": registered_user["password"]}
        )
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 200, response.text
        assert body["refreshToken"]

    @allure.title("Вход с неверным email")
    def test_login_with_wrong_email_error(self, registered_user):
        payload = {
            "email": f"wrong_{registered_user['email']}",
            "password": registered_user["password"],
        }
        response = StellarBurgersApi.login_user(payload)
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 401, response.text
        assert body == {"success": False, "message": Messages.INCORRECT_CREDENTIALS}

    @allure.title("Вход с неверным паролем")
    def test_login_with_wrong_password_error(self, registered_user):
        payload = {
            "email": registered_user["email"],
            "password": f"wrong_{registered_user['password']}",
        }
        response = StellarBurgersApi.login_user(payload)
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 401, response.text
        assert body == {"success": False, "message": Messages.INCORRECT_CREDENTIALS}

    @allure.title("Вход с неверными email и паролем")
    def test_login_with_wrong_email_and_password_error(self, registered_user):
        payload = {
            "email": f"wrong_{registered_user['email']}",
            "password": f"wrong_{registered_user['password']}",
        }
        response = StellarBurgersApi.login_user(payload)
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 401, response.text
        assert body == {"success": False, "message": Messages.INCORRECT_CREDENTIALS}
