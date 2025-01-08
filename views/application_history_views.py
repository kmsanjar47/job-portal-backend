from controllers.application_history_controller import ApplicationHistoryController
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi import Depends
from repository.database import get_db
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/get-application-history-by-user/{token}")
async def get_application_history_by_user(token: str, db: Session = Depends(get_db)):
    result = await ApplicationHistoryController.get_application_history_by_user(token, db)
    return result


@router.get("/get-application-history-by-job/{token}/{job_id}")
async def get_application_history_by_job(
    job_id: int, token: str, db: Session = Depends(get_db)
):
    application_history_with_user_info = await ApplicationHistoryController.get_application_history_by_job(
        token, db, job_id
    )
    return application_history_with_user_info


@router.get("/get-all-created-job-application-history/{token}")
async def get_all_created_job_application_history(
    token: str, db: Session = Depends(get_db)
):
    application_history_with_user_info = await ApplicationHistoryController.get_all_created_job_application_history(
        token, db)

    return application_history_with_user_info


@router.patch("/update-application-history/{token}/{job_id}/{user_id}/{status}")
async def update_application_history(
    job_id: int,
    user_id: str,
    status: str,
    token: str,
    db: Session = Depends(get_db),
):

    result = await ApplicationHistoryController.update_application_history(
        job_id, user_id, status, token, db
    )
    return result