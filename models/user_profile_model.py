from datetime import datetime
import uuid
from repository.database import Base
from sqlalchemy import Column, String, UUID, Boolean, ForeignKey, DateTime
from pydantic import BaseModel, EmailStr
import models.user_model
import models.job_model


class UserProfile(Base):
    __tablename__ = "user_profile"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey(models.user_model.User.id), nullable=False
    )
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    graduation_date = Column(DateTime, nullable=True, default=None)
    profile_photo = Column(String, nullable=True)
    resume = Column(String, nullable=True)
    department = Column(String, nullable=True)
    saved_jobs = Column(ForeignKey(models.job_model.Job.id), nullable=True)


class UserProfileCreate(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    user_id: str
    # graduation_date: datetime
    profile_photo: str
    resume: str
    department: str
    saved_jobs: int


class UserProfileResponse(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    # graduation_date: datetime
    profile_photo: str
    resume: str
    department: str
    saved_jobs: int

    class Config:
        from_attributes = True  # This replaces `orm_mode` in Pydantic v2
        arbitrary_types_allowed = True  # Allow arbitrary types
