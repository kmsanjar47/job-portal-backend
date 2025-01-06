from datetime import datetime
import shutil
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Form,
    File,
    UploadFile,
    Request,
)
from fastapi import Depends
from fastapi.responses import JSONResponse
from models.job_model import Job, JobCreate
from models.saved_jobs_model import SavedJobsModel
from repository.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select as Select
from utils import auth
from views.auth_views import get_current_user
from models.notifications_model import Notifications
from models.user_profile_model import UserProfile
from typing import Optional


router = APIRouter()

@router.get("/notification-by-user/{token}")
async def read_notification_by_user(token: str, db: Session = Depends(get_db)):
    user = await get_current_user(token, db)
    user_id = user.id
    # use sqlalchemy to get all jobs
    notifications = db.query(Notifications).filter(Notifications.user_id == user_id).all()
    return notifications