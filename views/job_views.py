from fastapi import APIRouter, Depends, HTTPException, status
from models.job_model import Job
from repository.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select as Select



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


@router.post("/jobs")
async def create_job(job: Job, db: Session = Depends(get_db)):
    db.add(job)
    db.commit()
    db.refresh(job)
    return job