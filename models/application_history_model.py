# Table ApplicationHistory{
#   user_id varchar
#   job_id varchar
#   status numeric [note: "Accepted, Rejected, Resume Downlaoded"]
# }

from sqlalchemy import Column, Integer, ForeignKey
from repository.database import Base
from pydantic import BaseModel
import models.user_model
import models.job_model

enum = {
    "Applied": 1,
    "Accepted": 2,
    "Rejected": 3,
    "Resume Downloaded": 4
}


class ApplicationHistory(Base):
    __tablename__ = "application_history"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey(models.user_model.User.id), nullable=False)
    job_id = Column(ForeignKey(models.job_model.Job.id), nullable=False)
    status = Column(Integer, nullable=False)


class ApplicationHistoryCreate(BaseModel):
    user_id: int
    job_id: int
    status: int


class ApplicationHistoryResponse(BaseModel):
    user_id: int
    job_id: int
    status: int

    class Config:
        from_attributes = True  # This replaces `orm_mode` in Pydantic v2
        arbitrary_types_allowed = True  # Allow arbitrary types
