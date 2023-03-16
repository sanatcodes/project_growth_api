import uuid
from pydantic import BaseModel, Field, validator


class Category(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    trending_date: str = Field(...)
    category_id: str = Field(...)
    views: int = Field(...)
    likes: int = Field(...)
    comment_count: int = Field(...)
    videos: int = Field(...)

    class Config:
        allow_population_by_field_name = False
        schema_extra = {
            'example': {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "trending_date": "2023-02-23",
                "category_id": "1",
                "views": 97100993,
                "likes": 4081644,
                "comment_count": 13244,
                "videos": 4
            }
        }


class Predictions(BaseModel):
    category_id: int
    year: int
    month: int
    day: int
    day_of_week: int

    @validator('year')
    def year_validator(cls, v):
        if v < 1900 or v > 2100:
            raise ValueError('year must be between 1900 and 2100')
        return v

    @validator('month')
    def month_validator(cls, v):
        if v < 1 or v > 12:
            raise ValueError('month must be between 1 and 12')
        return v

    @validator('day')
    def day_validator(cls, v, values):
        year = values.get('year')
        month = values.get('month')
        if v < 1 or v > 31:
            raise ValueError('day must be between 1 and 31')
        if month in [4, 6, 9, 11] and v > 30:
            raise ValueError('day must be between 1 and 30 for this month')
        if month == 2 and (v > 29 or (v == 29 and not year % 4 == 0)):
            raise ValueError(
                'day must be between 1 and 29 for this year and month')
        return v

    class Config:
        allow_population_by_field_name = False
        schema_extra = {
            'example': {
                "category_id": "1",
                "year": "2017",
                "month": "1",
                "day": "1",
                "day_of_week": "1"
            }
        }
