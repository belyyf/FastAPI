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


@app.get("/products", response_model=list[ProductResponse])
def get_products(
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    in_stock: Optional[bool] = None,
):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(status_code=400, detail="min_price должен быть <= max_price")

    result = list(products_db.values())

    if min_price is not None:
        result = [p for p in result if p["price"] >= min_price]
    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]
    if in_stock is not None:
        result = [p for p in result if p["in_stock"] == in_stock]

    return result


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_db[product_id]
