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
from fastapi.responses import JSONResponse
from models.job_model import Job, JobCreate
from repository.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select as Select
from utils import auth

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


@router.post("/jobs/")
async def create_job(
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
    token = request.headers.get("Authorization")
    token = token.split("Bearer ")[1]
    id = auth.verify_token(token)

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
        created_by=id,  # Assuming you have a logged-in user (ID = 1 for example)
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    # Add to the database and commit
    db.add(job)
    db.commit()
    db.refresh(job)

    return JSONResponse(
        content={"message": "Job created successfully", "job_id": job.id},
        status_code=201,
    )
