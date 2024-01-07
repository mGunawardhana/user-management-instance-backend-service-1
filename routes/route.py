from fastapi import APIRouter, HTTPException,status
from models.todos import Todo
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=dict)
async def root():
    return {"message": "Hello From Phoenix Instance"}


@router.get("/fetch-all-users", response_model=dict)
async def get_todos():
    try:
        todos = list_serial(collection_name.find())
        return {"data": todos, "message": "Successfully fetched todos", "status_code": 200}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch todos: {str(e)}",
        )


@router.post("/create-user", response_model=dict)
async def post_todo(todo: Todo):
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


@router.delete("/user/{user_id}", response_model=dict)
async def delete_todo(todo_id: str):
    try:
        result = collection_name.delete_one({"_id": todo_id})

        if result.deleted_count == 1:
            return {
                "data": {"id": todo_id},
                "message": "Todo deleted successfully",
                "status_code": 200
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with ID {todo_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete todo: {str(e)}"
        )