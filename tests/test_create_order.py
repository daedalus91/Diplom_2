import allure

from data import INVALID_INGREDIENT_HASH, NONEXISTENT_INGREDIENT_HASH, Messages
from helpers import extract_ingredient_ids
from stellar_api import StellarBurgersApi


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией: успешный ответ")
    def test_create_order_with_auth_returns_success(self, registered_user, order_ingredients):
        response = StellarBurgersApi.create_order(
            order_ingredients["ids"], registered_user["access_token"]
        )
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 200, response.text
        assert body["success"] is True

    @allure.title("Создание заказа с авторизацией: возвращается числовой номер заказа")
    def test_create_order_with_auth_returns_order_number(self, registered_user, order_ingredients):
        response = StellarBurgersApi.create_order(
            order_ingredients["ids"], registered_user["access_token"]
        )
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 200, response.text
        assert isinstance(body["order"]["number"], int)

    @allure.title("Создание заказа с авторизацией: заказ привязан к владельцу")
    def test_create_order_with_auth_returns_owner_email(self, registered_user, order_ingredients):
        response = StellarBurgersApi.create_order(
            order_ingredients["ids"], registered_user["access_token"]
        )
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 200, response.text
        assert body["order"]["owner"]["email"] == registered_user["email"]

    @allure.title("Создание заказа с авторизацией: цена равна сумме цен ингредиентов")
    def test_create_order_with_auth_calculates_expected_price(
        self, registered_user, order_ingredients
    ):
        response = StellarBurgersApi.create_order(
            order_ingredients["ids"], registered_user["access_token"]
        )
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 200, response.text
        assert body["order"]["price"] == order_ingredients["expected_price"]

    @allure.title("Создание заказа с авторизацией: в заказе сохраняются переданные ингредиенты")
    def test_create_order_with_auth_returns_ordered_ingredients(
        self, registered_user, order_ingredients
    ):
        response = StellarBurgersApi.create_order(
            order_ingredients["ids"], registered_user["access_token"]
        )
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 200, response.text
        assert extract_ingredient_ids(body["order"]) == order_ingredients["ids"]

    @allure.title("Создание заказа без авторизации запрещено")
    def test_create_order_without_auth_error(self, order_ingredients):
        response = StellarBurgersApi.create_order(order_ingredients["ids"])
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 401, response.text
        assert body == {"success": False, "message": Messages.UNAUTHORIZED}

    @allure.title("Создание заказа с авторизацией без ингредиентов")
    def test_create_order_with_auth_without_ingredients_error(self, registered_user):
        response = StellarBurgersApi.create_order([], registered_user["access_token"])
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 400, response.text
        assert body == {"success": False, "message": Messages.NO_INGREDIENTS}

    @allure.title("Создание заказа без авторизации и без ингредиентов")
    def test_create_order_without_auth_without_ingredients_error(self):
        response = StellarBurgersApi.create_order([])
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 400, response.text
        assert body == {"success": False, "message": Messages.NO_INGREDIENTS}

    @allure.title("Создание заказа с авторизацией и невалидным форматом хеша ингредиентов")
    def test_create_order_with_auth_and_invalid_hash_format_error(self, registered_user):
        response = StellarBurgersApi.create_order(
            [INVALID_INGREDIENT_HASH], registered_user["access_token"]
        )

        assert response.status_code == 500, response.text
        assert Messages.INTERNAL_SERVER_ERROR in response.text

    @allure.title("Создание заказа без авторизации и с невалидным форматом хеша ингредиентов")
    def test_create_order_without_auth_and_invalid_hash_format_error(self):
        response = StellarBurgersApi.create_order([INVALID_INGREDIENT_HASH])

        assert response.status_code == 500, response.text
        assert Messages.INTERNAL_SERVER_ERROR in response.text

    @allure.title("Создание заказа с авторизацией и несуществующим 24-hex хешем ингредиентов")
    def test_create_order_with_auth_and_nonexistent_hash_error(self, registered_user):
        response = StellarBurgersApi.create_order(
            [NONEXISTENT_INGREDIENT_HASH], registered_user["access_token"]
        )
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 400, response.text
        assert body == {"success": False, "message": Messages.INCORRECT_INGREDIENT_IDS}

    @allure.title("Создание заказа без авторизации и с несуществующим 24-hex хешем ингредиентов")
    def test_create_order_without_auth_and_nonexistent_hash_error(self):
        response = StellarBurgersApi.create_order([NONEXISTENT_INGREDIENT_HASH])
        body = StellarBurgersApi.safe_json(response)

        assert response.status_code == 400, response.text
        assert body == {"success": False, "message": Messages.INCORRECT_INGREDIENT_IDS}
