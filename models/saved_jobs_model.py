from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from repository.database import Base
from pydantic import BaseModel
import models.user_model
import models.job_model


class SavedJobsModel(Base):
    __tablename__ = 'saved_jobs'
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(models.user_model.User.id))
    job_id = Column(Integer, ForeignKey(models.job_model.Job.id))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class SavedJobsCreate(BaseModel):
    user_id: int
    job_id: int


class SavedJobsResponse(BaseModel):
    user_id: int
    job_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True