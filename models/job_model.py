from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from repository.database import Base
from pydantic import BaseModel
import models.user_model
import models.category_model

class Job(Base):
    __tablename__ = "job"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_by = ForeignKey(models.user_model.User.id)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False,default=datetime.now())
    updated_at = Column(DateTime, nullable=False,default=datetime.now())
    company_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    category = ForeignKey(models.category_model.Category.id, nullable=False)
    status = Column(Integer, nullable=False)
    documents = Column(String, nullable=True)

class JobCreate(BaseModel):
    title: str
    description: str
    company_name: str
    location: str
    category: str
    status: int
    documents: str
    # created_at: DateTime
    # updated_at: DateTime

class JobResponse(BaseModel):
    title: str
    description: str
    company_name: str
    location: str
    category: str
    status: int
    documents: str
    # created_at: DateTime
    # updated_at: DateTime

    class Config:
        from_attributes = True  # This replaces `orm_mode` in Pydantic v2
        arbitrary_types_allowed = True  # Allow arbitrary types