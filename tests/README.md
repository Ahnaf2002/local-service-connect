# Tests for Sheba APP

This directory contains pytest tests for the Sheba APP application.

## Running Tests

### Install test dependencies

```bash
pip install pytest pytest-cov
```

### Run all tests

```bash
pytest
pytest -v              # Verbose output
pytest --tb=short      # Shorter traceback
```

### Run specific test file

```bash
pytest tests/test_auth.py
pytest tests/test_models.py
```

### Run specific test class or function

```bash
pytest tests/test_auth.py::TestAuth
pytest tests/test_auth.py::TestAuth::test_login_valid
```

### Generate coverage report

```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

## Test Structure

- **`conftest.py`** — Pytest fixtures (app, client, auth_user, etc.) used by all tests
- **`test_auth.py`** — Authentication and authorization tests
- **`test_models.py`** — (To be added) Database model tests
- **`test_payments.py`** — (To be added) Payment route tests
- **`test_admin.py`** — (To be added) Admin dashboard tests

## Writing New Tests

### Example test structure

```python
class TestMyFeature:
    """Test description"""
    
    def test_specific_behavior(self, client, auth_user):
        """Test that something works as expected"""
        # Arrange
        data = {'key': 'value'}
        
        # Act
        response = client.post('/endpoint', data=data)
        
        # Assert
        assert response.status_code == 200
        assert b'expected text' in response.data
```

### Common fixtures

- **`app`** — Flask test app instance (testing config, in-memory SQLite DB)
- **`client`** — Test client for making HTTP requests
- **`runner`** — CLI command runner
- **`auth_user`** — Pre-created test user (email: `test@example.com`, password: `testpass123`)

### Example: test authenticated endpoint

```python
def test_admin_dashboard(self, client, auth_user):
    """Test admin can access dashboard"""
    # Login as user
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    # Access admin page
    response = client.get('/admin/dashboard')
    # Non-admin users should be redirected
    assert response.status_code in (403, 302)
```

## Continuous Integration

Tests run automatically on every PR and push to `main` via GitHub Actions (`.github/workflows/ci.yml`).

Check the Actions tab on GitHub to see test results.

## Coverage Goals

- Aim for >80% code coverage
- All public routes should have at least one test
- All model methods with business logic should be tested
- Auth decorators and permission checks should be tested
