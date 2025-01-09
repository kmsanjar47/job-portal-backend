from datetime import datetime
import shutil
from controllers.user_profile_controller import UserProfileController
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


@router.get("/user-profile/{token}")
async def read_user_profile(token: str, db: Session = Depends(get_db)):
    user = await get_current_user(token, db)
    user_id = user.id
    # use sqlalchemy to get all jobs
    user = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    return user


@router.post("/user-profile/")
async def create_user_profile(
    token: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(...),
    graduation_date: datetime = Form(...),
    profile_photo: UploadFile = File(...),
    resume: UploadFile = File(...),
    department: str = Form(...),
    saved_jobs: int = Form(...),
    db: Session = Depends(get_db),
):
    response = await UserProfileController.create_user_profile(
        token, name, email, phone_number, graduation_date, profile_photo, resume, department, saved_jobs, db
    )
    return response



@router.patch("/user-profile/{token}")
async def update_user_profile(
    token: str,
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    graduation_date: Optional[datetime] = Form(None),
    profile_photo: Optional[UploadFile] = File(None),
    resume: Optional[UploadFile] = File(None),
    department: Optional[str] = Form(None),
    saved_jobs: Optional[int] = Form(None),
    db: Session = Depends(get_db),
):
    response = await UserProfileController.update_user_profile(
        token, name, email, phone_number, graduation_date, profile_photo, resume, department, saved_jobs, db
    )

    return response
