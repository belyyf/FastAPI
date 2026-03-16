from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

app = FastAPI()

# In-memory хранилища
products_db: dict[int, dict] = {}
products_counter = 0
