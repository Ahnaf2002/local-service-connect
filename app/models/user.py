from datetime import datetime
from app.extensions import db
from sqlalchemy import Index
from .base import IdMixin, TimestampMixin
from .role import user_roles

class User(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "users"

    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    phone = db.Column(db.String(32), nullable=True, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=True)  # Nullable for social-only accounts
    full_name = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True, index=True)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    locale = db.Column(db.String(10), nullable=True)
    avatar_url = db.Column(db.String(1024), nullable=True)

    # social auth / external provider links (store provider name + provider user id)
    social_accounts = db.relationship("SocialAccount", back_populates="user", cascade="all,delete-orphan")

    # roles (many-to-many)
    roles = db.relationship("Role", secondary=user_roles, back_populates="users")

    # If the user is also a provider, ProviderProfile points to this user
    provider_profile = db.relationship("ProviderProfile", uselist=False, back_populates="user")

    bookings = db.relationship("Booking", back_populates="user", cascade="all,delete-orphan")
    orders = db.relationship("Order", back_populates="user", cascade="all,delete-orphan")
    reviews = db.relationship("Review", back_populates="user", cascade="all,delete-orphan")
    notifications = db.relationship("Notification", back_populates="user", cascade="all,delete-orphan")
    subscriptions = db.relationship("Subscription", back_populates="user", cascade="all,delete-orphan")

Index('ix_users_email_phone', User.email, User.phone)
