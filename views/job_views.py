from datetime import datetime
import shutil
from controllers.job_controller import JobController
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
from models.application_history_model import ApplicationHistory
from models.job_model import Job, JobCreate
from models.saved_jobs_model import SavedJobsModel
from repository.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select as Select
from utils import auth
from views.auth_views import get_current_user
from models.notifications_model import Notifications

# from auth_views import get_current_user


router = APIRouter()


@router.get("/jobs/{token}")
async def read_jobs(token: str, db: Session = Depends(get_db)):
    # use sqlalchemy to get all jobs
    # check apllication history to see if user has applied for jobs
    result = await JobController.read_jobs(token, db)
    return result


@router.get("/jobs/{job_id}")
async def read_job(job_id: int, db: Session = Depends(get_db)):
    job = await JobController.read_job(job_id, db)
    return job


@router.get("/jobs/search/{query}")
async def read_job(query: str, db: Session = Depends(get_db)):
    job = await JobController.search_job(query, db)
    return job


@router.post("/jobs/")
async def create_job(
    token: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    company_name: str = Form(...),
    location: str = Form(...),
    category: int = Form(...),
    status: int = Form(...),
    documents: UploadFile = File(None),
    request: Request = None,  # Optional file upload
    db: Session = Depends(get_db),
):
    # Decode token and get the user id
    response = await JobController.create_job(
        token, title, description, company_name, location, category, status, db
    )


    return response


@router.post("/jobs/saved-by-user/{job_id}")
async def save_job_by_user(
    job_id: int, auth_token: str = Form(...), db: Session = Depends(get_db)
):
    message = await JobController.save_job_by_user(job_id, auth_token, db)

    return message


@router.get("/jobs/saved-by-user/{token}")
async def get_saved_jobs_by_user(token: str, db: Session = Depends(get_db)):
    jobs = await JobController.get_saved_jobs_by_user(token, db)

    return jobs


@router.post("/jobs/apply/{token}/{job_id}")
async def apply_for_job(token: str, job_id: int, db: Session = Depends(get_db)):
    message = await JobController.apply_for_job(token, job_id, db)

    return message
