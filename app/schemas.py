from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, EmailStr, Field

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    results: list[T]
    total: int
    skip: int
    limit: int


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80, examples=["Notebook"])
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(gt=0, examples=[12.5])
    tags: list[str] = Field(default_factory=list)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Notebook",
                    "description": "Hardcover A5",
                    "price": 12.5,
                    "tags": ["stationery"],
                }
            ]
        }
    )


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=80)
    description: str | None = Field(default=None, max_length=500)
    price: float | None = Field(default=None, gt=0)
    tags: list[str] | None = None


class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    tags: list[str] = Field(default_factory=list)


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80, examples=["Grace Hopper"])
    email: EmailStr
    role: Literal["admin", "member"] = "member"

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Grace Hopper",
                    "email": "grace@example.com",
                    "role": "member",
                }
            ]
        }
    )


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Literal["admin", "member"]
