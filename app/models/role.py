from app.extensions import db
from .base import IdMixin, TimestampMixin

user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    db.Column("created_at", db.DateTime, nullable=False, default=db.func.utc_timestamp())
)

class Role(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "roles"

    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    description = db.Column(db.String(255), nullable=True)

    users = db.relationship("User", secondary=user_roles, back_populates="roles")
