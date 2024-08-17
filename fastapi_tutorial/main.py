from fastapi import Body, Cookie, FastAPI, Header, Path, Query
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl
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


# Path Parameters and Numeric Validations
# In the same way that you can declare more validations and metadata for query parameters with Query, you can declare the same type of validations and metadata for path parameters with Path.


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# Number validations: greater than or equal/ less than or equal
# item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)]
# size: Annotated[float, Query(gt=0, lt=10.5)]


# Body Parameters : another JSON object- Nested Model
# Body also has all the same extra validation and metadata parameters as Query,Path
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/body/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results


# field from pydantic model
class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/field/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results


# You can use Pydantic's Field to declare extra validations and metadata for model attributes.
# You can also use the extra keyword arguments to pass additional JSON Schema metadata.

# Nested Models:


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


@app.post("/offers/")
async def create_offer(offer: Offer) -> Offer:
    return offer


# Header and Cookie Parameters
@app.get("/header_cookies/")
def header_cookies(
    cookie_id: Annotated[str | None, Cookie()] = None,
    x_token: Annotated[str | None, Header()] = None,
    accept_encoding: Annotated[str | None, Header()] = None,
    accept_language: Annotated[str | None, Header()] = None,
    strange_header: Annotated[str | None, Header(convert_underscores=False)] = None,
):
    return {
        "cookie_id": cookie_id,
        "X-Token": x_token,
        "accept_encoding": accept_encoding,
        "accept_language": accept_language,
        "strange_header": strange_header,
    }
