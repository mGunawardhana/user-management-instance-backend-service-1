from fastapi import APIRouter, HTTPException,status
from models.todos import Todo
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=dict)
async def root():
    return {"message": "Hello From Phoenix Instance"}

@router.get("/todos", response_model=dict)
async def get_todos():
    try:
        todos = list_serial(collection_name.find())
        return {"data": todos, "message": "Successfully fetched todos", "status_code": 200}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch todos: {str(e)}",
        )
    
    
@router.post("/todos")
async def create_todos(todo: Todo):
    collection_name.insert_one(dict(todo))
    return dict(todo)