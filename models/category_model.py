# Table Category{
#   id varchar [primary key]
#   name varchar
#   created_at datetime
# }

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from repository.database import Base
from pydantic import BaseModel

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False,default=datetime.now())

class CategoryCreate(BaseModel):

    name: str
    # created_at: DateTime

class CategoryResponse(BaseModel):
    name: str
    # created_at: DateTime

    class Config:
        from_attributes = True  # This replaces `orm_mode` in Pydantic v2
        arbitrary_types_allowed = True  # Allow arbitrary types