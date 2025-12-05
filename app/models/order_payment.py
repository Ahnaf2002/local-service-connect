from app.extensions import db
from .base import IdMixin, TimestampMixin
import enum

class OrderStatus(enum.Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"

class PaymentGateway(enum.Enum):
    bkash = "bkash"
    nagad = "nagad"
    card = "card"
    other = "other"

class PaymentStatus(enum.Enum):
    pending = "pending"
    succeeded = "succeeded"
    failed = "failed"
    refunded = "refunded"
    cancelled = "cancelled"

class Order(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "orders"

    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    total_amount = db.Column(db.Numeric(12,2), nullable=False, default=0.0)
    currency = db.Column(db.String(8), nullable=False, default="BDT")
    status = db.Column(db.Enum(OrderStatus, values_callable=lambda obj: [e.value for e in obj]), nullable=False, default=OrderStatus.pending.value, index=True)
    order_metadata = db.Column(db.JSON, nullable=True)

    payments = db.relationship("Payment", back_populates="order", cascade="all,delete-orphan")
    booking = db.relationship("Booking", back_populates="order")
    user = db.relationship("User", back_populates="orders")

class Payment(db.Model, IdMixin, TimestampMixin):
    __tablename__ = "payments"

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    provider_id = db.Column(db.Integer, db.ForeignKey("provider_profiles.id", ondelete="SET NULL"), nullable=True, index=True)

    gateway = db.Column(db.Enum(PaymentGateway, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    method = db.Column(db.String(50), nullable=True)  # card, wallet, bank_transfer
    external_transaction_id = db.Column(db.String(255), nullable=True, index=True)
    amount = db.Column(db.Numeric(12,2), nullable=False)
    currency = db.Column(db.String(8), nullable=False, default="BDT")
    status = db.Column(db.Enum(PaymentStatus, values_callable=lambda obj: [e.value for e in obj]), nullable=False, default=PaymentStatus.pending.value, index=True)
    gateway_response = db.Column(db.JSON, nullable=True)

    order = db.relationship("Order", back_populates="payments")
    booking = db.relationship("Booking", backref="payments")
    user = db.relationship("User")
    provider = db.relationship("ProviderProfile")
