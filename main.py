from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes.route import router

app = FastAPI()

origins = [
    "http://localhost:3000",
    # Add any other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["*"],
)

app.include_router(router)
