from app.extensions import db
from .base import IdMixin, TimestampMixin

class SocialAccount(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "social_accounts"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    provider = db.Column(db.String(50), nullable=False)  # e.g., 'google', 'facebook'
    provider_user_id = db.Column(db.String(255), nullable=False, index=True)
    profile_data = db.Column(db.JSON, nullable=True)  # raw provider profile
    linked_at = db.Column(db.DateTime, nullable=False, default=db.func.utc_timestamp())

    user = db.relationship("User", back_populates="social_accounts")

    __table_args__ = (db.UniqueConstraint("provider", "provider_user_id", name="uq_social_provider_user"),)
