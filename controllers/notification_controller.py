from models.notifications_model import Notifications
from views.auth_views import get_current_user


class NotificationController:

    @staticmethod
    async def read_notification_by_user(token, db):
        user = await get_current_user(token, db)
        user_id = user.id
        # use sqlalchemy to get all jobs
        notifications = db.query(Notifications).filter(Notifications.user_id == user_id).all()
        return notifications