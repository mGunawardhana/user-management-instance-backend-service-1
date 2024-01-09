def individual_serial(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "mobile": user["mobile"],
        "password": user["password"],
        "re_type_password": user["re_type_password"],
        "country": user["country"],
        "country_code": user["country_code"],
        "address": user["address"],
        "notes": user["notes"],
    }


def list_serial(users) -> list:
    return [individual_serial(user) for user in users]
