from datetime import datetime
import shutil
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
    categories = db.query(Category).all()
    return categories


@router.get("/categories/{category_id}")
async def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    return category


@router.post("/categories/")
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
):
    new_category = Category(name=category.name, created_at=datetime.now())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
