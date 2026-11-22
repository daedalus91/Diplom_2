import uuid


def generate_user():
    unique = uuid.uuid4().hex[:12]
    return {
        "email": f"test_user_{unique}@example.com",
        "password": f"Pass_{unique}",
        "name": f"User {unique[:6]}",
    }


def extract_ingredient_ids(order):
    return [item["_id"] for item in order["ingredients"]]
