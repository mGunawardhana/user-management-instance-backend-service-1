from fastapi import APIRouter, HTTPException, status
from models.users import User
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId
from loguru import logger

router = APIRouter()

def handle_exception(e, message):
    """
    Handle exceptions by logging and raising an HTTPException.

    Args:
        e (Exception): The exception object.
        message (str): A custom error message.

    Raises:
        HTTPException: An exception with a 500 Internal Server Error status code.
    """
    logger.error(f"{message}: {str(e)}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"{message}: {str(e)}"
    )

@router.get("/", response_model=dict)
async def root():
    """
    Root endpoint.

    Returns:
        dict: A response message.
    """
    logger.info("Root endpoint accessed")
    return {"message": "Hello From Phoenix Instance"}

@router.get("/fetch-all-users", response_model=dict)
async def fetch_all_users():
    """
    Fetch all users.

    Returns:
        dict: A response with user data.
    """
    try:
        users = list_serial(collection_name.find())
        return {"data": users, "message": "Successfully fetched users", "status_code": 200}
    except Exception as e:
        handle_exception(e, "Failed to fetch users")

@router.post("/create-user", response_model=dict)
async def create_user(user: User):
    """
    Create a new user.

    Args:
        user (User): User data.

    Returns:
        dict: A response with user creation status.
    """
    try:
        inserted_id = collection_name.insert_one(dict(user)).inserted_id
        return inserted_id and {"data": {"id": str(inserted_id)},
                                "message": "User created successfully", "status_code": 201}
    except Exception as e:
        handle_exception(e, "Failed to create user")

@router.put("/{user_id}", response_model=dict)
async def update_user(user_id: str, user: User):
    """
    Update an existing user.

    Args:
        user_id (str): User ID.
        user (User): Updated user data.

    Returns:
        dict: A response with user update status.
    """
    try:
        result = collection_name.find_one_and_update({"_id": ObjectId(user_id)}, {"$set": dict(user)})
        return result and {"data": {"id": user_id},
                           "message": "User updated successfully", "status_code": 200}
    except Exception as e:
        handle_exception(e, f"Failed to update user")

@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    """
    Delete an existing user.

    Args:
        user_id (str): User ID.

    Returns:
        dict: A response with user deletion status.
    """
    try:
        result = collection_name.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count == 1 and {"data": {"id": user_id},
                                              "message": "User deleted successfully", "status_code": 200}
    except Exception as e:
        handle_exception(e, f"Failed to delete user")

@router.get("/{user_id}", response_model=dict)
async def get_user_by_id(user_id: str):
    """
    Get user by ID.

    Args:
        user_id (str): User ID.

    Returns:
        dict: A response with user data.
    """
    try:
        user_data = collection_name.find_one({"_id": ObjectId(user_id)})
        return user_data and {"data": user_data,
                              "message": "User retrieved successfully", "status_code": 200}
    except Exception as e:
        handle_exception(e, f"Failed to retrieve user")

