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
