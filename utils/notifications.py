from sqlalchemy.orm import Session
from models.notification_model import Notifications
from repository.database import SessionLocal

async def send_notification(user, message):
    # Send a notification to the user
    db = SessionLocal()
    notification = Notifications(user_id=user.id, message=message)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    print(f"Notification sent to {user.username}")