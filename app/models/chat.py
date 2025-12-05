from app.extensions import db
from .base import IdMixin, TimestampMixin

class Conversation(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "conversations"

    # Link to booking if this conversation belongs to a booking
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True, index=True)

    # Usually between a user and a provider; store both for fast lookup
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    provider_id = db.Column(db.Integer, db.ForeignKey("provider_profiles.id", ondelete="CASCADE"), nullable=False, index=True)

    last_message_at = db.Column(db.DateTime, nullable=True, index=True)

    user = db.relationship("User")
    provider = db.relationship("ProviderProfile")
    messages = db.relationship("Message", back_populates="conversation", cascade="all,delete-orphan")

class Message(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "messages"

    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = db.Column(db.Text, nullable=True)
    attachment_url = db.Column(db.String(1024), nullable=True)
    read = db.Column(db.Boolean, nullable=False, default=False, index=True)
    sent_at = db.Column(db.DateTime, nullable=False, default=db.func.utc_timestamp())

    conversation = db.relationship("Conversation", back_populates="messages")
    sender = db.relationship("User")
