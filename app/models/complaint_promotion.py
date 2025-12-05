from app.extensions import db
from .base import IdMixin, TimestampMixin
import enum

class ComplaintStatus(enum.Enum):
    opened = "opened"
    in_review = "in_review"
    resolved = "resolved"
    dismissed = "dismissed"

class Complaint(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "complaints"

    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    reported_provider_id = db.Column(db.Integer, db.ForeignKey("provider_profiles.id", ondelete="SET NULL"), nullable=True, index=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(4096), nullable=True)
    status = db.Column(db.Enum(ComplaintStatus, values_callable=lambda obj: [e.value for e in obj]), nullable=False, default=ComplaintStatus.opened.value, index=True)
    resolution_notes = db.Column(db.String(4096), nullable=True)
    resolved_by_admin_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    resolved_at = db.Column(db.DateTime, nullable=True)

class PromotionType(enum.Enum):
    banner = "banner"
    featured = "featured"
    boosted = "boosted"

class Promotion(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "promotions"

    provider_id = db.Column(db.Integer, db.ForeignKey("provider_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    type = db.Column(db.Enum(PromotionType, values_callable=lambda obj: [e.value for e in obj]), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=True)
    promotion_data = db.Column(db.JSON, nullable=True)  # creative, target area, etc.
    start_date = db.Column(db.DateTime, nullable=False, index=True)
    end_date = db.Column(db.DateTime, nullable=False, index=True)
    active = db.Column(db.Boolean, nullable=False, default=True, index=True)

    provider = db.relationship("ProviderProfile", back_populates="promotions")
