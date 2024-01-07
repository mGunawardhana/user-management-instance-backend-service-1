from fastapi import APIRouter, HTTPException, status
from models.todos import Todo
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()


@router.get("/", response_model=dict)
async def root():
    return {"message": "Hello From Phoenix Instance"}


@router.get("/fetch-all-users", response_model=dict)
async def fetch_all_users():
    try:
        todos = list_serial(collection_name.find())
        return {"data": todos, "message": "Successfully fetched todos", "status_code": 200}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch todos: {str(e)}",
        )


@router.post("/create-user", response_model=dict)
async def create_user(todo: Todo):
    try:
        inserted_id = collection_name.insert_one(dict(todo)).inserted_id
        if inserted_id:
            return {
                "data": {"id": str(inserted_id)},
                "message": "Todo created successfully",
                "status_code": 201
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create todo"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create todo: {str(e)}"
        )


@router.put("/{user_id}", response_model=dict)
async def update_user(user_id: str, todo: Todo):
    try:
        # Convert the user_id to ObjectId for querying MongoDB
        user_object_id = ObjectId(user_id)

        # Perform the update operation
        result = collection_name.find_one_and_update(
            {"_id": user_object_id},
            {"$set": dict(todo)}
        )

        if result:
            return {
                "data": {"id": user_id},
                "message": "User updated successfully",
                "status_code": 200
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )

@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    try:
        # Convert the user_id to ObjectId for querying MongoDB
        user_object_id = ObjectId(user_id)

        # Perform the delete operation
        result = collection_name.delete_one({"_id": user_object_id})

        if result.deleted_count == 1:
            return {
                "data": {"id": user_id},
                "message": "User deleted successfully",
                "status_code": 200
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        )
