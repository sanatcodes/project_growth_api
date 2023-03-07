from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import pandas as pd
import pickle

from models import Category, Predictions

router = APIRouter()


@router.post("/", response_description="Create a new category", status_code=status.HTTP_201_CREATED, response_model=Category)
def create_categories(request: Request, categories: List[Category] = Body(...)):
    # convert the list of categories to a list of dictionaries
    categories_dict = jsonable_encoder(categories)

    # insert the list of categories into the MongoDB collection
    inserted_ids = request.app.database["fypProjectGrowth"].insert_many(
        categories_dict).inserted_ids

    # create a new list of categories with the generated IDs
    new_categories = []
    for i in range(len(categories)):
        new_category = categories[i].dict()
        new_category["_id"] = str(inserted_ids[i])
        new_categories.append(new_category)

    # print(new_categories)

    return {"message": "Categories created successfully", "inserted_ids": new_categories}


@router.get("/", response_description="List all categories", response_model=List[Category])
def list_categories(request: Request):
    categories = list(request.app.database["fypProjectGrowth"].find(limit=100))
    return categories


@router.get("/{trending_date}", response_description="Get a single category by id", response_model=List[Category])
def find_category(trending_date: str, request: Request):
    filtered_categoryies = list(
        request.app.database["fypProjectGrowth"].find({"trending_date": trending_date}))
    if len(filtered_categoryies) > 0:
        return filtered_categoryies
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with date {trending_date} not found")


# import models
with open('yt-views-0.3.0.pk1', 'rb') as f:
    viewsModel = pickle.load(f)

with open('yt-likes-0.3.0.pk1', 'rb') as f:
    likesModel = pickle.load(f)

with open('yt-videos-0.3.0.pk1', 'rb') as f:
    videosModel = pickle.load(f)


@router.post('/predict')
async def predict_all_endpoint(item: Predictions):
    try:
        item_dict = item.dict()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail='Invalid input data: ' + str(e))

    # Additional input validation logic goes here

    df = pd.DataFrame([item_dict.values()], columns=item_dict.keys())
    views_prediction = viewsModel.predict(df)
    likes_prediction = likesModel.predict(df)
    videos_prediction = videosModel.predict(df)
    return {
        'views_prediction': int(views_prediction),
        'likes_prediction': int(likes_prediction),
        'videos_prediction': int(videos_prediction)
    }
