from fastapi import APIRouter
from models.todos import Todo
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

@router.get("/todos")
async def get_todos():
    todos = list_serial(collection_name.find())
    return todos

@router.post("/todos")
async def create_todos(todo: Todo):
    collection_name.insert_one(dict(todo))
    return dict(todo)