from flask import Flask
from config import config
from app.extensions import db, migrate, login_manager
from dotenv import load_dotenv
import os

load_dotenv()

def create_app(config_name=None):
    """Application factory function"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Register blueprints
    from app.auth import auth_bp
    from app.admin import admin_bp
    from app.payments import payments_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(payments_bp)
    
    # Register shell context for flask shell
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': __import__('app.models', fromlist=['User']).User,
            'Order': __import__('app.models', fromlist=['Order']).Order,
            'Payment': __import__('app.models', fromlist=['Payment']).Payment,
        }
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
