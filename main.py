from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import app_router
import uvicorn
from database.db import create_tables
from fastapi.staticfiles import StaticFiles
from api.algorithms import alg_router
app = FastAPI()
app.include_router(app_router)
app.include_router(alg_router)
create_tables()
origins = [
    "http://localhost:5173",
    "localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#app.mount('/media', StaticFiles(directory='media'),name='media')

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port = 8000)