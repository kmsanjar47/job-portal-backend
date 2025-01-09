from datetime import datetime
import shutil
from controllers.category_controller import CategoryController
from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from fastapi.responses import JSONResponse
from models.category_model import Category, CategoryCreate, CategoryResponse
from repository.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select as Select


router = APIRouter()


@router.get("/categories")
async def read_categories(db: Session = Depends(get_db)):
    # use sqlalchemy to get all categories
    categories = CategoryController.read_categories(db)
    return categories


@router.get("/categories/{category_id}")
async def read_category(category_id: int, db: Session = Depends(get_db)):
    category = CategoryController.read_category(category_id, db)
    return category


@router.post("/categories/")
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
):
    new_category = CategoryController.create_category(category, db)
    return new_category
