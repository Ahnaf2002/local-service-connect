from app.extensions import db
from .base import IdMixin, TimestampMixin
import enum

class VerificationStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class ProviderVerification(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "provider_verifications"

    provider_id = db.Column(db.Integer, db.ForeignKey("provider_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    submitted_documents = db.Column(db.JSON, nullable=True)
    status = db.Column(db.Enum(VerificationStatus, values_callable=lambda obj: [e.value for e in obj]), nullable=False, default=VerificationStatus.pending.value, index=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.String(2048), nullable=True)

    provider = db.relationship("ProviderProfile", back_populates="verifications")
