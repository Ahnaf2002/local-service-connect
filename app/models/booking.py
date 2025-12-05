from app.extensions import db
from .base import IdMixin, TimestampMixin
import enum

class BookingStatus(enum.Enum):
    requested = "requested"
    accepted = "accepted"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"
    rejected = "rejected"
    no_show = "no_show"

class Booking(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "bookings"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    provider_id = db.Column(db.Integer, db.ForeignKey("provider_profiles.id", ondelete="SET NULL"), nullable=True, index=True)
    provider_service_id = db.Column(db.Integer, db.ForeignKey("provider_services.id", ondelete="SET NULL"), nullable=True, index=True)

    # Booking times
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime, nullable=True, index=True)

    # pricing snapshot (denormalized for historical accuracy)
    currency = db.Column(db.String(8), nullable=False, default="BDT")
    price = db.Column(db.Numeric(10,2), nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=True)

    status = db.Column(db.Enum(BookingStatus, values_callable=lambda obj: [e.value for e in obj]), nullable=False, default=BookingStatus.requested.value, index=True)
    provider_note = db.Column(db.String(2048), nullable=True)
    user_note = db.Column(db.String(2048), nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    order = db.relationship("Order", uselist=False, back_populates="booking")
    user = db.relationship("User", back_populates="bookings")
    provider = db.relationship("ProviderProfile", back_populates="bookings")
    provider_service = db.relationship("ProviderService", backref="bookings")
    reviews = db.relationship("Review", back_populates="booking", cascade="all,delete-orphan")
