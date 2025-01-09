from datetime import datetime
from models.category_model import Category


class CategoryController:

    @staticmethod
    def read_categories(db):
        return db.query(Category).all()
    
    @staticmethod
    def read_category(category_id, db):
        return db.query(Category).filter(Category.id == category_id).first()
    
    @staticmethod
    def create_category(category, db):
        new_category = Category(name=category.name, created_at=datetime.now())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category