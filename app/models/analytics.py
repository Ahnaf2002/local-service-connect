from app.extensions import db
from .base import IdMixin, TimestampMixin

class AnalyticsEvent(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "analytics_events"

    event_type = db.Column(db.String(128), nullable=False, index=True)
    actor_id = db.Column(db.Integer, nullable=True, index=True)  # optional user id or provider id
    actor_type = db.Column(db.String(32), nullable=True)  # 'user' or 'provider' or 'system'
    booking_id = db.Column(db.Integer, nullable=True, index=True)
    provider_id = db.Column(db.Integer, nullable=True, index=True)
    payload = db.Column(db.JSON, nullable=True)  # event-specific data

    # useful index for queries by type/time
    __table_args__ = (db.Index('ix_analytics_event_time', 'event_type', 'created_at'),)
