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
    user = await get_current_user(token, db)
    user_id = user.id
    # use sqlalchemy to get all jobs
    user_profile = UserProfile(
        user_id=user_id,
        name=name,
        email=email,
        phone_number=phone_number,
        graduation_date=graduation_date,
        profile_photo=profile_photo,
        resume=resume,
        department=department,
        saved_jobs=saved_jobs,
    )
    db.add(user_profile)
    db.commit()
    db.refresh(user_profile)

    notification = Notifications(
        user_id=user_id,
        message="User profile created successfully",
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)

    return {
        "message": "User profile created successfully",
        "data": user_profile,
    }



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
    user = await get_current_user(token, db)
    if not user:
        return {"error": "Invalid token"}

    user_profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    if not user_profile:
        user_profile = UserProfile(user_id=user.id)
        db.add(user_profile)
        db.commit()
        db.refresh(user_profile)

        notification = Notifications(
            user_id=user.id,
            message="User profile created successfully",
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)

    if name:
        user_profile.name = name
    if email:
        user_profile.email = email
    if phone_number:
        user_profile.phone_number = phone_number
    if graduation_date:
        user_profile.graduation_date = graduation_date
    if profile_photo:
        document_filename = (
            f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_{profile_photo.filename}"
        )
        with open(document_filename, "wb") as buffer:
            shutil.copyfileobj(profile_photo.file, buffer)
        user_profile.profile_photo = document_filename
    if resume:
        document_filename = (
            f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_{resume.filename}"
        )
        with open(document_filename, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        user_profile.resume = document_filename
    if department:
        user_profile.department = department
    if saved_jobs:
        user_profile.saved_jobs = saved_jobs

    db.commit()

    notification = Notifications(
        user_id=user.id,
        message="User profile updated successfully",
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)

    return {
        "message": "User profile updated successfully",
        "data": {
            "name": user_profile.name,
            "email": user_profile.email,
            "phone_number": user_profile.phone_number,
            "graduation_date": user_profile.graduation_date,
            "profile_photo": user_profile.profile_photo,
            "resume": user_profile.resume,
            "department": user_profile.department,
            "saved_jobs": user_profile.saved_jobs,
        },
    }
