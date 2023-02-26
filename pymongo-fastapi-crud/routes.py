from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Category

router = APIRouter()


# @router.post("/", response_description="Create a new category", status_code=status.HTTP_201_CREATED, response_model=Category)
# def create_category(request: Request, category: Category = Body(...)):
#     category = jsonable_encoder(category)
#     new_category = request.app.database["fypProjectGrowth"].insertMany(category)

#     return {"message": "Categories created successfully", "inserted_ids": new_category.inserted_ids}

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


@router.get("/{trending_date}", response_description="Get a single category by id", response_model=Category)
def find_category(trending_date: str, request: Request):
    if (category := request.app.database["fypProjectGrowth"].find_one({"trending_date": trending_date})) is not None:
        return category
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Category with date {trending_date} not found")
