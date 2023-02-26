import uuid
from pydantic import BaseModel, Field


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
