from models.notifications_model import Notifications
from models.user_profile_model import UserProfile
from views.auth_views import get_current_user


class UserProfileController:

    @staticmethod
    async def create_user_profile(token, name, email, phone_number, graduation_date, profile_photo, resume, department, saved_jobs, db):
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
    
    @staticmethod
    async def update_user_profile(token, name, email, phone_number, graduation_date, profile_photo, resume, department, saved_jobs, db):
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
    
    @staticmethod
    async def read_user_profile(token, db):
        user = await get_current_user(token, db)
        user_id = user.id
        # use sqlalchemy to get all jobs
        user_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        return user_profile
    
    @staticmethod
    async def read_user_profile_by_id(user_id, db):
        user_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        return user_profile
    
    @staticmethod
    async def read_all_user_profiles(db):
        return db.query(UserProfile).all()
    
    @staticmethod
    async def delete_user_profile(token, db):
        user = await get_current_user(token, db)
        user_id = user.id
        user_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        db.delete(user_profile)
        db.commit()
        return {"message": "User profile deleted successfully"}