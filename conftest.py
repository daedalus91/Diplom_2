import allure
import pytest

from helpers import generate_user
from stellar_api import StellarBurgersApi


def _delete_user_finalizer(access_token):
    with allure.step("Постусловие: удалить тестового пользователя"):
        response = StellarBurgersApi.delete_user(access_token)
        response.raise_for_status()


@pytest.fixture
def user_data():
    return generate_user()


@pytest.fixture
def register_user_request(request):

    def _register(payload):
        response = StellarBurgersApi.create_user(payload)
        body = StellarBurgersApi.safe_json(response)
        if isinstance(body, dict) and body.get("accessToken"):
            token = body["accessToken"]
            request.addfinalizer(lambda: _delete_user_finalizer(token))
        return response

    return _register


@pytest.fixture
def registered_user(request, user_data):
    response = StellarBurgersApi.create_user(user_data)
    access_token = response.json()["accessToken"]
    request.addfinalizer(lambda: _delete_user_finalizer(access_token))
    return {**user_data, "access_token": access_token}


@pytest.fixture(scope="session")
def order_ingredients():
    items = StellarBurgersApi.get_ingredients().json()["data"]
    bun = next(item for item in items if item["type"] == "bun")
    filling = next(item for item in items if item["type"] != "bun")
    return {
        "ids": [bun["_id"], filling["_id"]],
        "expected_price": bun["price"] + filling["price"],
    }
