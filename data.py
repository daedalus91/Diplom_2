import os

BASE_URL = os.getenv("STELLAR_BURGERS_URL", "https://stellarburgers.education-services.ru").rstrip("/")


class Urls:
    REGISTER = f"{BASE_URL}/api/auth/register"
    LOGIN = f"{BASE_URL}/api/auth/login"
    USER = f"{BASE_URL}/api/auth/user"
    ORDERS = f"{BASE_URL}/api/orders"
    INGREDIENTS = f"{BASE_URL}/api/ingredients"


class Messages:
    USER_ALREADY_EXISTS = "User already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"
    INCORRECT_CREDENTIALS = "email or password are incorrect"
    NO_INGREDIENTS = "Ingredient ids must be provided"
    INCORRECT_INGREDIENT_IDS = "One or more ids provided are incorrect"
    UNAUTHORIZED = "You should be authorised"
    INTERNAL_SERVER_ERROR = "Internal Server Error"


INVALID_INGREDIENT_HASH = "invalid_ingredient_hash_123"
NONEXISTENT_INGREDIENT_HASH = "000000000000000000000000"

MISSING_REQUIRED_FIELD_CASES = [
    ({"password": "TestPassword123", "name": "Test User"}, "email"),
    ({"email": "missing_password@example.com", "name": "Test User"}, "password"),
    ({"email": "missing_name@example.com", "password": "TestPassword123"}, "name"),
]

EMPTY_REQUIRED_FIELD_CASES = [
    ({"email": "", "password": "TestPassword123", "name": "Test User"}, "email"),
    ({"email": "empty_password@example.com", "password": "", "name": "Test User"}, "password"),
    ({"email": "empty_name@example.com", "password": "TestPassword123", "name": ""}, "name"),
]
