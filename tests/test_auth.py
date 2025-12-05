"""
Test suite for Local Service Connect

Run tests with:
    pytest                  # Run all tests
    pytest -v               # Verbose output
    pytest tests/test_auth.py   # Run specific test file
    pytest --cov=app        # Show coverage report
"""

import pytest


class TestIndex:
    """Test home/index route"""
    
    def test_index_not_authenticated(self, client):
        """Test index page for unauthenticated users"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Sheba APP' in response.data
        assert b'Looking for Services' in response.data
    
    def test_index_authenticated(self, client, auth_user):
        """Test index page for authenticated users"""
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'testpass123'
        }, follow_redirects=True)
        
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome' in response.data


class TestAuth:
    """Test authentication routes"""
    
    def test_register_page(self, client):
        """Test register page loads"""
        response = client.get('/auth/register')
        assert response.status_code == 200
        assert b'Create Account' in response.data
    
    def test_login_page(self, client):
        """Test login page loads"""
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'Login' in response.data
    
    def test_register_valid(self, client):
        """Test user registration with valid data"""
        response = client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'is_provider': False
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Account created successfully' in response.data
    
    def test_register_duplicate_email(self, client, auth_user):
        """Test registration with duplicate email"""
        response = client.post('/auth/register', data={
            'username': 'anotheruser',
            'email': 'test@example.com',  # same as auth_user
            'password': 'password123',
            'confirm_password': 'password123'
        })
        
        assert response.status_code == 200
        assert b'already registered' in response.data or b'Email' in response.data
    
    def test_login_valid(self, client, auth_user):
        """Test login with valid credentials"""
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'testpass123',
            'remember_me': False
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Welcome' in response.data
    
    def test_login_invalid_password(self, client, auth_user):
        """Test login with invalid password"""
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Invalid email or password' in response.data
    
    def test_logout(self, client, auth_user):
        """Test user logout"""
        # Login first
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'testpass123'
        }, follow_redirects=True)
        
        # Logout
        response = client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'logged out' in response.data


class TestModels:
    """Test database models"""
    
    def test_user_creation(self, app):
        """Test creating a user"""
        with app.app_context():
            user = User(username='testuser', email='test@test.com')
            user.set_password('password123')
            assert user.verify_password('password123')
            assert not user.verify_password('wrongpassword')
    
    def test_user_roles(self, app):
        """Test user role assignments"""
        with app.app_context():
            customer = User(username='customer', email='c@test.com', is_provider=False)
            provider = User(username='provider', email='p@test.com', is_provider=True)
            admin = User(username='admin', email='a@test.com', is_admin=True)
            
            assert not customer.is_provider
            assert provider.is_provider
            assert admin.is_admin


# Import User model for tests
from app.models import User
