from sqlalchemy import Column, String, UUID, Boolean
from repository.database import Base
from pydantic import BaseModel, EmailStr
import uuid


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    is_general_user = Column(Boolean, default=True)


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_general_user: bool


class UserResponse(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # This replaces `orm_mode` in Pydantic v2
        arbitrary_types_allowed = True  # Allow arbitrary types


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    email: EmailStr
    is_general_user: bool
