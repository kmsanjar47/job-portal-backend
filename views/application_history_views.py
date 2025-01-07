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
from models.application_history_model import ApplicationHistory
from typing import Optional


router = APIRouter()


@router.get("/get-application-history-by-user/{token}")
async def get_application_history_by_user(token: str, db: Session = Depends(get_db)):
    user = await get_current_user(token, db)
    user_id = user.id

    application_history = (
        db.query(ApplicationHistory).filter(ApplicationHistory.user_id == user_id).all()
    )

    return application_history


@router.get("/get-application-history-by-job/{token}/{job_id}")
async def get_application_history_by_job(
    job_id: int, token: str, db: Session = Depends(get_db)
):
    user = await get_current_user(token, db)
    user_id = user.id

    is_created_by_user = (
        db.query(Job).filter(Job.created_by == user_id).filter(Job.id == job_id).all()
    )
    print(is_created_by_user)

    if not is_created_by_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to view this application history",
        )
    application_history_with_user_info = []
    application_history = (
        db.query(ApplicationHistory).filter(ApplicationHistory.job_id == job_id).all()
    )

    for application in application_history:
        user_profile = (
            db.query(UserProfile)
            .filter(UserProfile.user_id == application.user_id)
            .first()
        )
        application_history_with_user_info.append(
            {
                "user_id": application.user_id,
                "job_id": application.job_id,
                "status": application.status,
                "user_info": user_profile,
                "job_data": db.query(Job).filter(Job.id == application.job_id).first(),
            }
        )

    return application_history_with_user_info


@router.get("/get-all-created-job-application-history/{token}")
async def get_all_created_job_application_history(
    token: str, db: Session = Depends(get_db)
):
    user = await get_current_user(token, db)
    user_id = user.id

    created_jobs = db.query(Job).filter(Job.created_by == user_id).all()
    application_history_with_user_info = []
    for job in created_jobs:
        application_history = (
            db.query(ApplicationHistory)
            .filter(ApplicationHistory.job_id == job.id)
            .all()
        )
        for application in application_history:
            user_profile = (
                db.query(UserProfile)
                .filter(UserProfile.user_id == application.user_id)
                .first()
            )
            application_history_with_user_info.append(
                {
                    "user_id": application.user_id,
                    "job_id": application.job_id,
                    "status": application.status,
                    "user_info": user_profile,
                    "job_data": db.query(Job)
                    .filter(Job.id == application.job_id)
                    .first(),
                }
            )

    return application_history_with_user_info


@router.patch("/update-application-history/{token}/{job_id}/{user_id}/{status}")
async def update_application_history(
    job_id: int,
    user_id: str,
    status: str,
    token: str,
    db: Session = Depends(get_db),
):

    enum = {
        "Applied": 1,
        "Accepted": 2,
        "Rejected": 3,
        "Resume Downloaded": 4,
    }

    user = await get_current_user(token, db)
    user_id = user.id

    is_created_by_user = (
        db.query(Job).filter(Job.created_by == user_id).filter(Job.id == job_id).all()
    )

    if not is_created_by_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to update this application history",
        )

    application_history = (
        db.query(ApplicationHistory)
        .filter(ApplicationHistory.job_id == job_id)
        .filter(ApplicationHistory.user_id == user_id)
        .first()
    )

    if not application_history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application history not found",
        )

    application_history.status = enum[status]

    db.commit()

    # send notification to user

    notification = Notifications(
        user_id=user_id,
        message=f"Application status updated for job: {job_id} \n New status: {status}",
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)

    return {
        "message": "Application status updated successfully",
        "job_id": job_id,
        "user_id": user_id,
        "status": status,
    }
