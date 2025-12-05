from app.extensions import db
from .base import IdMixin, TimestampMixin

class ServiceCategory(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "service_categories"

    name = db.Column(db.String(150), nullable=False, index=True)
    slug = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("service_categories.id", ondelete="SET NULL"), nullable=True)

    parent = db.relationship("ServiceCategory", remote_side=[IdMixin.id], backref="children")

class Service(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "services"

    name = db.Column(db.String(150), nullable=False, index=True)
    slug = db.Column(db.String(150), nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey("service_categories.id", ondelete="SET NULL"), nullable=True, index=True)
    description = db.Column(db.String(1024), nullable=True)

    category = db.relationship("ServiceCategory", backref="services")

class ProviderService(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "provider_services"

    provider_id = db.Column(db.Integer, db.ForeignKey("provider_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True)

    # Pricing model: support fixed price and hourly
    fixed_price = db.Column(db.Numeric(10,2), nullable=True)
    hourly_rate = db.Column(db.Numeric(10,2), nullable=True)
    currency = db.Column(db.String(8), nullable=False, default="BDT", index=True)
    duration_minutes = db.Column(db.Integer, nullable=True)  # typical duration
    active = db.Column(db.Boolean, nullable=False, default=True, index=True)
    details = db.Column(db.String(2048), nullable=True)

    provider = db.relationship("ProviderProfile", back_populates="services")
    service = db.relationship("Service", backref="provider_links")

    __table_args__ = (db.UniqueConstraint('provider_id', 'service_id', name='uq_provider_service'),)
