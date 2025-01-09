from controllers.auth_controller import AuthController
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models.user_model
from repository.database import engine, get_db
import models.user_model as models, utils.auth as auth
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=models.UserResponse)
async def register_user(user: models.UserCreate, db: Session = Depends(get_db)):
    new_user = await AuthController.register(user, db)
    return new_user


@router.post("/login", response_model=models.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    data = await AuthController.login(form_data, db)
    return data


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    user = await AuthController.get_current_user(token, db)
    return user


@router.get("/users/me", response_model=models.UserResponse)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user
