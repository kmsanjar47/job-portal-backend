# Table Messages{
#   user_id_one varchar
#   user_id_two varchar
# }

from uuid import UUID
from sqlalchemy import Column, Integer, ForeignKey, String
from repository.database import Base
from pydantic import BaseModel
import models.user_model


class Messages(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id_one = Column(ForeignKey(models.user_model.User.id), nullable=False)
    user_id_two = Column(ForeignKey(models.user_model.User.id), nullable=False)


class MessagesCreate(BaseModel):
    user_id_one: int
    user_id_two: int


class MessagesResponse(BaseModel):
    user_id_one: int
    user_id_two: int

    class Config:
        from_attributes = True  # This replaces `orm_mode` in Pydantic v2
        arbitrary_types_allowed = True  # Allow arbitrary types
