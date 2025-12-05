from app.extensions import db
from .base import IdMixin, TimestampMixin
import enum

class NotificationChannel(enum.Enum):
    email = "email"
    sms = "sms"
    web = "web"

class NotificationType(enum.Enum):
    booking_update = "booking_update"
    offer = "offer"
    subscription = "subscription"
    system = "system"

class Notification(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "notifications"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    channel = db.Column(db.Enum(NotificationChannel, values_callable=lambda obj: [e.value for e in obj]), nullable=False, index=True)
    type = db.Column(db.Enum(NotificationType, values_callable=lambda obj: [e.value for e in obj]), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=True)
    body = db.Column(db.String(2048), nullable=True)
    payload = db.Column(db.JSON, nullable=True)  # structured data to support deep links, etc.
    sent = db.Column(db.Boolean, nullable=False, default=False, index=True)
    sent_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="notifications")
