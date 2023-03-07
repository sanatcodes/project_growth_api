from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as category_router
from fastapi.middleware.cors import CORSMiddleware
import pickle 
import pandas as pd

# api setup
config = dotenv_values(".env")

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(category_router, tags=["categories"], prefix="/category")
