import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    """Create and configure a test app instance."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's CLI commands."""
    return app.test_cli_runner()

@pytest.fixture
def auth_user(app):
    """Create a test user for authentication tests."""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            is_admin=False,
            is_provider=False
        )
        user.set_password('testpass123')
        db.session.add(user)
        db.session.commit()
        return user
