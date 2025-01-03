# Table Notifications{
#   user_id varchar
#   message varchar
#   created_at datetime
# }
from datetime import datetime
from uuid import UUID
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from repository.database import Base
from pydantic import BaseModel
import models.user_model


class Notifications(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey(models.user_model.User.id), nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())


class NotificationsCreate(BaseModel):
    user_id: int
    message: str
    # created_at: DateTime


class NotificationsResponse(BaseModel):
    user_id: int
    message: str
    # created_at: DateTime

    class Config:
        from_attributes = True  # This replaces `orm_mode` in Pydantic v2
        arbitrary_types_allowed = True  # Allow arbitrary types
