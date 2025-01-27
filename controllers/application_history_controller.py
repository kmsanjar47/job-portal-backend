from models.application_history_model import ApplicationHistory
from models.job_model import Job
from models.notifications_model import Notifications
from models.user_profile_model import UserProfile
from views.auth_views import get_current_user
from fastapi import status,HTTPException

class ApplicationHistoryController:
    @staticmethod
    async def get_application_history_by_user(token,db):
        user = await get_current_user(token, db)
        user_id = user.id

        result = []

        application_history = (
            db.query(ApplicationHistory).filter(ApplicationHistory.user_id == user_id).all()
        )
        enum = {
            1: "Applied",
            2: "Accepted",
            3: "Rejected",
            4: "Resume Downloaded",
        }
        for application in application_history:
            result.append(
                {
                    "user_id": application.user_id,
                    "job_id": application.job_id,
                    "status": enum[application.status],
                    "job_data": db.query(Job).filter(Job.id == application.job_id).first(),
                }
            )
        return result
    
    @staticmethod
    async def get_application_history_by_job(token,db,job_id):
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
    
    @staticmethod
    async def get_all_created_job_application_history(token,db):
        user = await get_current_user(token, db)
        user_id = user.id

        created_jobs = db.query(Job).filter(Job.created_by == user_id).all()
        application_history_with_user_info = []
        user_profiles = []
        for job in created_jobs:
            application_history = (
                db.query(ApplicationHistory)
                .filter(ApplicationHistory.job_id == job.id)
                .distinct(ApplicationHistory.user_id)
            )

            user_profiles = []

            for application in application_history:
                user_profile = (
                    db.query(UserProfile)
                    .filter(UserProfile.user_id == application.user_id)
                    .first()
                )
                status = (
                    application_history.filter(
                        ApplicationHistory.user_id == application.user_id
                    )
                    .filter(ApplicationHistory.job_id == job.id)
                    .first()
                    .status
                )

                user_profile.__setattr__("status", status)

                user_profiles.append(user_profile)

            application_history_with_user_info.append(
                {
                    "user_id": application.user_id,
                    "job_id": job.id,
                    "user_info": user_profiles,
                    "job_data": job,
                }
            )
        return application_history_with_user_info
    
    @staticmethod
    async def update_application_history(job_id,user_id,status,token,db):
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
