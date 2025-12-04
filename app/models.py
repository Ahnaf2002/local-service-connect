from datetime import datetime
from app.extensions import db, login_manager
from flask_login import UserMixin
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class User(UserMixin, db.Model):
    """User model with role-based access"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_provider = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    orders = db.relationship('Order', backref='customer', lazy=True, foreign_keys='Order.user_id')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = pwd_context.hash(password)
    
    def verify_password(self, password):
        """Verify password against hash"""
        return pwd_context.verify(password, self.password_hash)
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for login manager"""
    return User.query.get(int(user_id))

class Order(db.Model):
    """Order model for service requests"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, completed, cancelled
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    payment = db.relationship('Payment', backref='order', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.id}>'

class Payment(db.Model):
    """Payment model for order transactions"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, completed, failed
    payment_method = db.Column(db.String(50), default='stripe')
    transaction_id = db.Column(db.String(255), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Payment {self.id}>'

# === MEMBER 2 FUNCTIONALITY WILL BE ADDED HERE ===
# Member 2 will add:
# - Profile model (user profiles, verification, ratings)
# - ServiceListing model (services offered by providers)
# - Notification model (for alerts and messages)

# === MEMBER 3 FUNCTIONALITY WILL BE ADDED HERE ===
# Member 3 will add:
# - Booking model (service bookings and scheduling)
# - Review model (customer reviews and ratings)
# - AdPromotion model (promotion campaigns)
# - Analytics model (usage statistics and reporting)

# === MEMBER 4 FUNCTIONALITY WILL BE ADDED HERE ===
# Member 4 will add:
# - Location model (geographic service areas)
# - Chat model (messaging between users and providers)
# - Verification model (document verification for providers)
# - Subscription model (membership tiers and billing)
