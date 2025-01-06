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

# from auth_views import get_current_user


router = APIRouter()


@router.get("/jobs")
async def read_jobs(db: Session = Depends(get_db)):
    # use sqlalchemy to get all jobs
    jobs = db.query(Job).all()
    return jobs


@router.get("/jobs/{job_id}")
async def read_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/jobs/search/{query}")
async def read_job(query: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.title.like(f"%{query}%")).all()
    print(job)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
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
    user = await get_current_user(token, db)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = user.id

    # Process the image file (if any)
    document_path = None
    if documents:
        document_filename = (
            f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_{documents.filename}"
        )
        with open(document_filename, "wb") as buffer:
            shutil.copyfileobj(documents.file, buffer)
        document_path = document_filename  # Save the file path

    

    # Create a new job instance
    job = Job(
        title=title,
        description=description,
        company_name=company_name,
        location=location,
        category=category,
        status=status,
        documents=document_path,  # Save file path to DB
        created_by=user_id,  # Assuming you have a logged-in user (ID = 1 for example)
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    # Add to the database and commit
    db.add(job)
    db.commit()
    db.refresh(job)

    notification = Notifications(user_id=job.created_by, message=f"Job created: {job.title}")
    db.add(notification)
    db.commit()
    db.refresh(notification)


    return JSONResponse(
        content={"message": "Job created successfully", "job_id": job.id},
        status_code=201,
    )

@router.post("/jobs/saved-by-user/{job_id}")
async def save_job_by_user(job_id: int,auth_token : str=Form(...), db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if db.query(SavedJobsModel).filter(SavedJobsModel.job_id == job_id).first():
        raise HTTPException(status_code=200, detail="Job already saved")
    # Save the job to the user's saved jobs
    user = await get_current_user(auth_token, db)
    print(user)
    # user.saved_jobs.append(job)
    saved_job = SavedJobsModel(user_id=user.id, job_id=job_id)
    db.add(saved_job)
    db.commit()

    notification = Notifications(user_id=user.id, message=f"Job saved: {job.title}")
    db.add(notification)
    db.commit()
    db.refresh(notification)

    return {"message": "Job saved successfully"}


@router.get("/jobs/saved-by-user/{token}")
async def get_saved_jobs_by_user(token : str, db: Session = Depends(get_db)):
    user = await get_current_user(token, db)
    saved_jobs = db.query(SavedJobsModel).filter(SavedJobsModel.user_id == user.id).all()
    jobs = []
    for saved_job in saved_jobs:
        job = db.query(Job).filter(Job.id == saved_job.job_id).first()
        jobs.append(job)
    
    return jobs
    