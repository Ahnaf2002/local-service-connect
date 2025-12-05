from datetime import datetime
from app.extensions import db


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class IdMixin(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
