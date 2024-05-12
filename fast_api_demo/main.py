# This is demo hands-on code snippet for learning fastai
# Taken the reference from below blogs:
# https://fastapi.tiangolo.com/
# https://github.com/pixegami/simple-fastapi-example/blob/main/main.py

# Required libraries to install using pip : fastapi, uvicorn

# to launch the app by hitting the below command inside the project directory: uvicorn main:app --reload
# to launch the app in browser http://127.0.0.1:8000/
# and swagger http://127.0.0.1:8000/docs/ and http://127.0.0.1:8000/redoc

# Here the official documentation for fastapi : https://fastapi.tiangolo.com/tutorial/


from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Product(BaseModel):
    name: str
    price: int
    type: str


product_model: Dict[int, Product] = {}
product_seq = 0


@app.get("/")
def main_page() -> Dict[int, Product]:
    return product_model


@app.post("/product")
def add_product(products: List[Product]) -> Dict[int, Product]:
    global product_seq

    for product in products:
        product_model[product_seq] = product
        product_seq = product_seq + 1

    return product_model


@app.get("/product/{id}")
def get_product(id: int) -> Product:
    if id in product_model:
        return product_model[id]
    else:
        raise HTTPException(
            status_code=404, detail=f"Product id {id} not found"
        )


@app.delete("/product/{id}")
def delete_product(id: int) -> Product:
    if id in product_model:
        return product_model.pop(id)
    else:
        raise HTTPException(
            status_code=404, detail=f"Product id {id} not found"
        )
