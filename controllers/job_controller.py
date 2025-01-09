from datetime import datetime
import shutil
from models.application_history_model import ApplicationHistory
from models.job_model import Job
from models.notifications_model import Notifications
from models.saved_jobs_model import SavedJobsModel
from views.auth_views import get_current_user
from fastapi import HTTPException
from fastapi.responses import JSONResponse


class JobController:

    @staticmethod
    async def read_jobs(token, db):
        # use sqlalchemy to get all jobs
        # check apllication history to see if user has applied for jobs
        user = await get_current_user(token, db)
        user_id = user.id
        filtered_applied_job_ids = (
            db.query(ApplicationHistory)
            .filter(ApplicationHistory.user_id == user_id)
            .values(ApplicationHistory.job_id)
        )

        filtered_saved_job_ids = (
            db.query(SavedJobsModel)
            .filter(SavedJobsModel.user_id == user_id)
            .values(SavedJobsModel.job_id)
        )

        if not filtered_applied_job_ids:
            filtered_applied_job_ids = []
        else:
            filtered_applied_job_ids = [job_id[0] for job_id in filtered_applied_job_ids]
        if not filtered_saved_job_ids:
            filtered_saved_job_ids = []
        else:
            filtered_saved_job_ids = [job_id[0] for job_id in filtered_saved_job_ids]

        result = []
        jobs = db.query(Job).all()
        for job in jobs:
            if job.id not in filtered_applied_job_ids:
                result.append(
                    {
                        "id": job.id,
                        "title": job.title,
                        "description": job.description,
                        "company_name": job.company_name,
                        "location": job.location,
                        "category": job.category,
                        "status": job.status,
                        "documents": job.documents,
                        "created_by": job.created_by,
                        "created_at": job.created_at,
                        "updated_at": job.updated_at,
                        "applied": False,
                        "saved": job.id in filtered_saved_job_ids,
                    }
                )
            else:
                result.append(
                    {
                        "id": job.id,
                        "title": job.title,
                        "description": job.description,
                        "company_name": job.company_name,
                        "location": job.location,
                        "category": job.category,
                        "status": job.status,
                        "documents": job.documents,
                        "created_by": job.created_by,
                        "created_at": job.created_at,
                        "updated_at": job.updated_at,
                        "applied": True,
                        "saved": job.id in filtered_saved_job_ids,
                    }
                )

        return result
    
    @staticmethod
    async def read_job(job_id, db):
        job = db.query(Job).filter(Job.id == job_id).first()
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    
    @staticmethod
    async def read_job_by_query(query, db):
        job = db.query(Job).filter(Job.title.like(f"%{query}%")).all()
        print(job)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    
    @staticmethod
    async def create_job(token, title, description, company_name, location, category, status, documents, db):
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

        notification = Notifications(
            user_id=job.created_by, message=f"Job created: {job.title}"
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)

        return JSONResponse(
            content={"message": "Job created successfully", "job_id": job.id},
            status_code=201,
        )
    
    @staticmethod
    async def save_job_by_user(job_id, auth_token, db):
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
    
    @staticmethod
    async def get_saved_jobs_by_user(token, db):
        user = await get_current_user(token, db)
        saved_jobs = (
            db.query(SavedJobsModel).filter(SavedJobsModel.user_id == user.id).all()
        )
        jobs = []
        for saved_job in saved_jobs:
            job = db.query(Job).filter(Job.id == saved_job.job_id).first()
            jobs.append(job)

        return jobs
    
    @staticmethod
    async def apply_for_job(token, job_id, db):
        user = await get_current_user(token, db)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        application = ApplicationHistory(user_id=user.id, job_id=job_id, status=1)
        db.add(application)
        db.commit()

        notification = Notifications(user_id=user.id, message=f"Applied to job: {job_id}")
        db.add(notification)
        db.commit()
        db.refresh(notification)

        return {"message": "Applied for job successfully"}
    
    @staticmethod
    async def update_job(job_id, title, description, company_name, location, category, status, documents, db):
        job = db.query(Job).filter(Job.id == job_id).first()
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")

        # Process the image file (if any)
        document_path = None
        if documents:
            document_filename = (
                f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_{documents.filename}"
            )
            with open(document_filename, "wb") as buffer:
                shutil.copyfileobj(documents.file, buffer)
            document_path = document_filename  # Save the file path

        job.title = title
        job.description = description
        job.company_name = company_name
        job.location = location
        job.category = category
        job.status = status
        job.documents = document_path
        job.updated_at = datetime.now()

        db.commit()
        db.refresh(job)

        notification = Notifications(user_id=job.created_by, message=f"Job updated: {job.title}")
        db.add(notification)
        db.commit()
        db.refresh(notification)

        return JSONResponse(
            content={"message": "Job updated successfully", "job_id": job.id},
            status_code=200,
        )
    
    @staticmethod
    async def delete_job(job_id, db):
        job = db.query(Job).filter(Job.id == job_id).first()
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")

        db.delete(job)
        db.commit()

        return JSONResponse(
            content={"message": "Job deleted successfully", "job_id": job.id},
            status_code=200,
        )
    
    @staticmethod
    async def read_job_applications(job_id, db):
        applications = db.query(ApplicationHistory).filter(ApplicationHistory.job_id == job_id).all()
        return applications
