from fastapi import APIRouter, HTTPException, status
from models.users import User
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

def handle_exception(e, message):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"{message}: {str(e)}"
    )

@router.get("/", response_model=dict)
async def root():
    return {"message": "Hello From Phoenix Instance"}

@router.get("/fetch-all-users", response_model=dict)
async def fetch_all_users():
    try:
        users = list_serial(collection_name.find())
        return {"data": users, "message": "Successfully fetched todos", "status_code": 200}
    except Exception as e:
        handle_exception(e, "Failed to fetch todos")

@router.post("/create-user", response_model=dict)
async def create_user(user: User):
    try:
        inserted_id = collection_name.insert_one(dict(user)).inserted_id
        return inserted_id and {"data": {"id": str(inserted_id)},
                                "message": "Todo created successfully", "status_code": 201}
    except Exception as e:
        handle_exception(e, "Failed to create todo")

@router.put("/{user_id}", response_model=dict)
async def update_user(user_id: str, user: User):
    try:
        result = collection_name.find_one_and_update({"_id": ObjectId(user_id)}, {"$set": dict(user)})
        return result and {"data": {"id": user_id},
                           "message": "User updated successfully", "status_code": 200}
    except Exception as e:
        handle_exception(e, f"Failed to update user")

@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    try:
        result = collection_name.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count == 1 and {"data": {"id": user_id},
                                              "message": "User deleted successfully", "status_code": 200}
    except Exception as e:
        handle_exception(e, f"Failed to delete user")

@router.get("/{user_id}", response_model=dict)
async def get_user_by_id(user_id: str):
    try:
        user_data = collection_name.find_one({"_id": ObjectId(user_id)})
        return user_data and {"data": user_data,
                              "message": "User retrieved successfully", "status_code": 200}
    except Exception as e:
        handle_exception(e, f"Failed to retrieve user")