from app.extensions import db
from .base import IdMixin, TimestampMixin

class Review(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "reviews"

    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    provider_id = db.Column(db.Integer, db.ForeignKey("provider_profiles.id", ondelete="CASCADE"), nullable=False, index=True)

    rating = db.Column(db.Integer, nullable=False)  # 1-5
    title = db.Column(db.String(255), nullable=True)
    comment = db.Column(db.String(2048), nullable=True)
    is_public = db.Column(db.Boolean, nullable=False, default=True)
    edited_at = db.Column(db.DateTime, nullable=True)

    booking = db.relationship("Booking", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")
    provider = db.relationship("ProviderProfile", backref="reviews")

    __table_args__ = (db.UniqueConstraint('booking_id', 'user_id', name='uq_booking_user_review'),)
