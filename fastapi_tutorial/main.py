from fastapi import FastAPI, Query
from enum import Enum
from pydantic import BaseModel
from typing import Annotated


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/")
async def post():
    return {"message": "Hello from the post route"}


@app.put("/")
async def put():
    return {"message": "Hello from the put route"}


# to execute this file run command :
#  fastapi dev main.py
# or
#  uvicorn main:app --reload


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


# Path Parameters with Enums : endpoint /models/{model_name}
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# Query Parameters: Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Request and Response Body Models
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/")
async def create_item(item: Item):
    return item


# Annotations with Query Parameters: max_length parameter or min_length
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=5)] = None):
    # async def read_items(q: str | None = Query(default=None, max_length=50)): #Without annotations with default values
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Query parameter list / multiple values
# async def read_items(q: Annotated[list[str] | None, Query()] = None):
# http://localhost:8000/items/?q=foo&q=bar

# Generic validations and metadata:
# alias
# title
# description
# deprecated

# Validations specific for strings:
# min_length
# max_length
# pattern
# include_in_schema

# q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")] = None
#  valid patterns: ^fixedquery$
# This specific regular expression pattern checks that the received parameter value:
# ^: starts with the following characters, doesn't have characters before.
# fixedquery: has the exact value fixedquery.
# $: ends there, doesn't have any more characters after fixedquery.

# q: Annotated[
#     str | None,
#     Query(
#         alias="item-query",
#         title="Query string",
#         description="Query string for the items to search in the database that have a good match",
#         min_length=3,
#         max_length=50,
#         pattern="^fixedquery$",
#         deprecated=True,
#         include_in_schema=False
#     ),
# ] = None,
