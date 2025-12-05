from app.extensions import db
from .base import IdMixin, TimestampMixin
import enum

class SubscriptionStatus(enum.Enum):
    active = "active"
    cancelled = "cancelled"
    expired = "expired"
    paused = "paused"

class PremiumPlan(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "premium_plans"

    name = db.Column(db.String(255), nullable=False, index=True)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(2048), nullable=True)
    price = db.Column(db.Numeric(12,2), nullable=False, default=0.0)
    currency = db.Column(db.String(8), nullable=False, default="BDT")
    period = db.Column(db.String(20), nullable=False)  # 'monthly', 'yearly'
    benefits = db.Column(db.JSON, nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True, index=True)

class Subscription(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "subscriptions"

    # A subscription can belong to a user or provider. For simplicity we store both as nullable.
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    provider_id = db.Column(db.Integer, db.ForeignKey("provider_profiles.id", ondelete="CASCADE"), nullable=True, index=True)

    plan_id = db.Column(db.Integer, db.ForeignKey("premium_plans.id", ondelete="SET NULL"), nullable=True, index=True)
    start_date = db.Column(db.DateTime, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False, index=True)
    auto_renew = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.Enum(SubscriptionStatus, values_callable=lambda obj: [e.value for e in obj]), nullable=False, default=SubscriptionStatus.active.value, index=True)
    gateway_subscription_id = db.Column(db.String(255), nullable=True)
    subscription_metadata = db.Column(db.JSON, nullable=True)

    user = db.relationship("User", back_populates="subscriptions")
    provider = db.relationship("ProviderProfile", back_populates="subscriptions")
    plan = db.relationship("PremiumPlan")
