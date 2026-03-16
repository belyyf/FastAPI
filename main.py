from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

app = FastAPI()

# In-memory хранилища
products_db: dict[int, dict] = {}
products_counter = 0


# Products models
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    price: int = Field(..., ge=0)
    in_stock: bool = True


class ProductUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    price: int = Field(..., ge=0)
    in_stock: bool


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    in_stock: bool


@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate):
    global products_counter
    products_counter += 1
    product_data = {
        "id": products_counter,
        "name": product.name,
        "price": product.price,
        "in_stock": product.in_stock,
    }
    products_db[products_counter] = product_data
    return product_data
