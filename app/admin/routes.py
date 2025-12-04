from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.admin import admin_bp
from app.models import User, Order, Payment

def admin_required(f):
    """Decorator to check if user is admin"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard placeholder"""
    total_users = User.query.count()
    total_orders = Order.query.count()
    total_payments = Payment.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_orders=total_orders,
                         total_payments=total_payments,
                         pending_orders=pending_orders)

# === MEMBER 2 FUNCTIONALITY WILL BE ADDED HERE ===
# Admin routes for profile management and service listing approval

# === MEMBER 3 FUNCTIONALITY WILL BE ADDED HERE ===
# Admin routes for booking management and analytics

# === MEMBER 4 FUNCTIONALITY WILL BE ADDED HERE ===
# Admin routes for verification and subscription management
