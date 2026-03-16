from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, field_validator
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


@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")

    product_data = {
        "id": product_id,
        "name": product.name,
        "price": product.price,
        "in_stock": product.in_stock,
    }
    products_db[product_id] = product_data
    return product_data


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    del products_db[product_id]
    return {"message": "Product deleted"}


# ========== Задача 3: Students ==========
students_db: dict[int, dict] = {}
students_counter = 0


class StudentCreate(BaseModel):
    full_name: str = Field(..., min_length=5, max_length=120)
    group_name: str = Field(..., min_length=1, max_length=20)
    is_active: bool = True

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v):
        if " " not in v:
            raise ValueError("full_name должен содержать хотя бы пробел (имя и фамилия)")
        return v


class StudentUpdate(BaseModel):
    group_name: Optional[str] = Field(None, min_length=1, max_length=20)
    is_active: Optional[bool] = None


class StudentResponse(BaseModel):
    id: int
    full_name: str
    group_name: str
    is_active: bool


@app.post("/students", response_model=StudentResponse)
def create_student(student: StudentCreate):
    global students_counter
    students_counter += 1
    student_data = {
        "id": students_counter,
        "full_name": student.full_name,
        "group_name": student.group_name,
        "is_active": student.is_active,
    }
    students_db[students_counter] = student_data
    return student_data


@app.get("/students", response_model=list[StudentResponse])
def get_students(
    group_name: Optional[str] = None,
    is_active: Optional[bool] = None,
):
    result = list(students_db.values())

    if group_name is not None:
        result = [s for s in result if s["group_name"] == group_name]
    if is_active is not None:
        result = [s for s in result if s["is_active"] == is_active]

    return result


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[student_id]


@app.patch("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentUpdate):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")

    student_data = students_db[student_id]

    if student.group_name is not None:
        student_data["group_name"] = student.group_name
    if student.is_active is not None:
        student_data["is_active"] = student.is_active

    students_db[student_id] = student_data
    return student_data


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    del students_db[student_id]
    return {"message": "Student deleted"}


# ========== Задача 4: Pomodoro Presets ==========
presets_db: dict[int, dict] = {}
presets_counter = 0


class PresetCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=50)
    work_minutes: int = Field(..., ge=1, le=180)
    break_minutes: int = Field(..., ge=1, le=60)


class PresetUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=50)
    work_minutes: Optional[int] = Field(None, ge=1, le=180)
    break_minutes: Optional[int] = Field(None, ge=1, le=60)


class PresetResponse(BaseModel):
    id: int
    title: str
    work_minutes: int
    break_minutes: int
    created_at: datetime
