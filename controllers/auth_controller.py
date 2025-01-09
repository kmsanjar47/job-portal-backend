from fastapi import HTTPException,status
from models.user_model import User
from utils import auth
class AuthController:
    @staticmethod
    async def register(user,db):
        db_user = (
        db.query(User).filter(User.username == user.username).first()
        )
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        if not user.email.__contains__(".bracu"):
            raise HTTPException(status_code=400, detail="Not a valid BRACU email")
        hashed_password = auth.get_password_hash(user.password)
        new_user = User(
            username=user.username, email=user.email, hashed_password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @staticmethod
    async def login(form_data,db):
        user = (db.query(User).filter(User.username == form_data.username).first())
        if not user or not auth.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = auth.create_access_token(
            data={"sub": user.username, "id": str(user.id)}
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "username": user.username,
            "email": user.email,
            "is_general_user": user.is_general_user,
        }
    
    @staticmethod
    async def get_current_user(token,db):
        username = auth.verify_token(token)
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = db.query(models.User).filter(models.User.username == username).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")