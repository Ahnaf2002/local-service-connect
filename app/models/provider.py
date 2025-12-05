from app.extensions import db
from .base import IdMixin, TimestampMixin
from sqlalchemy import Index

class ProviderProfile(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "provider_profiles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    # Business fields
    display_name = db.Column(db.String(255), nullable=True)
    company_name = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.String(2048), nullable=True)
    profile_photo = db.Column(db.String(1024), nullable=True)

    # Location / service area
    address = db.Column(db.String(1024), nullable=True)
    city = db.Column(db.String(255), nullable=True, index=True)
    area = db.Column(db.String(255), nullable=True, index=True)  # area string if desired
    latitude = db.Column(db.Float, nullable=True, index=True)
    longitude = db.Column(db.Float, nullable=True, index=True)
    service_radius_km = db.Column(db.Float, nullable=True)  # optional radius

    # flags
    auto_accept = db.Column(db.Boolean, nullable=False, default=False, index=True)
    verified = db.Column(db.Boolean, nullable=False, default=False, index=True)
    rating_avg = db.Column(db.Float, nullable=True, default=0.0)
    rating_count = db.Column(db.Integer, nullable=False, default=0)

    # verification document(s)
    verification_documents = db.Column(db.JSON, nullable=True)

    user = db.relationship("User", back_populates="provider_profile")
    services = db.relationship("ProviderService", back_populates="provider", cascade="all,delete-orphan")
    bookings = db.relationship("Booking", back_populates="provider", cascade="all,delete-orphan")
    promotions = db.relationship("Promotion", back_populates="provider", cascade="all,delete-orphan")
    subscriptions = db.relationship("Subscription", back_populates="provider", cascade="all,delete-orphan")
    verifications = db.relationship("ProviderVerification", back_populates="provider", cascade="all,delete-orphan")

Index('ix_provider_geo', ProviderProfile.latitude, ProviderProfile.longitude)
