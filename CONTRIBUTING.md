# Contributing to Sheba APP

Thank you for being part of the Sheba APP team! This document outlines our contribution guidelines and workflow.

## Team Structure

| Member | Responsibilities | Areas |
|--------|------------------|-------|
| **Member 1** (Ahnaf2002) | Core Framework, Auth, Admin, Payments | `app/__init__.py`, `app/auth/`, `app/admin/`, `app/payments/` |
| **Member 2** | Profiles, Service Listings, Notifications | `app/profile/`, `app/services/`, `app/notifications/` |
| **Member 3** | Bookings, Reviews, Ad Promotions, Analytics | `app/bookings/`, `app/reviews/`, `app/analytics/` |
| **Member 4** | Location Search, Chat, Verification, Subscriptions | `app/location/`, `app/chat/`, `app/verification/`, `app/subscriptions/` |

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Ahnaf2002/local-service-connect.git
cd local-service-connect
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

```bash
cp .env.example .env
# Edit .env with your local MySQL credentials
```

### 5. Initialize Database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run Development Server

```bash
python run.py
# Server runs on http://localhost:5000
```

## Development Workflow

### 1. Create a Feature Branch

Always create a feature branch for your work:

```bash
git checkout -b feature/member2-profiles
# or
git checkout -b bugfix/member3-booking-issue
# or
git checkout -b docs/update-readme
```

Branch naming convention:
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test additions

### 2. Commit Messages

Write clear, descriptive commit messages:

```bash
# Good
git commit -m "Add user profile model and endpoints"
git commit -m "Fix payment webhook signature verification"
git commit -m "Update README with deployment instructions"

# Avoid
git commit -m "Updated stuff"
git commit -m "WIP"
git commit -m "asdf"
```

Format:
- Use present tense ("Add feature" not "Added feature")
- Be specific and descriptive
- Keep under 72 characters if possible
- Reference issue numbers if applicable: "Fixes #123"

### 3. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then on GitHub:
1. Create a Pull Request (PR)
2. Title: Clear description of changes
3. Description: What changed and why
4. Link related issues (use "Fixes #123" to auto-close)
5. Request code review from relevant team members (use CODEOWNERS)

### 4. Code Review & Merge

- At least one review approval before merge
- Address all review comments
- Ensure CI/CD tests pass
- Squash commits if needed (maintainer discretion)
- Delete branch after merge

## Coding Standards

### Python Style

Follow PEP 8:

```bash
# Check style with flake8 (optional, install with: pip install flake8)
flake8 app/

# Auto-format with black (optional, install with: pip install black)
black app/
```

### Code Structure

- Use blueprints for modular organization
- Write docstrings for all functions and classes
- Add type hints where possible
- Keep functions small and focused
- Use descriptive variable names

Example:

```python
def create_order(user_id: int, amount: float) -> Order:
    """
    Create a new service order.
    
    Args:
        user_id: ID of the customer placing the order
        amount: Order amount in dollars
        
    Returns:
        The newly created Order object
        
    Raises:
        ValueError: If amount is negative or user not found
    """
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    
    order = Order(user_id=user_id, amount=amount)
    db.session.add(order)
    db.session.commit()
    return order
```

### Database Models

- Always include timestamps: `created_at` and `updated_at`
- Use proper foreign keys and relationships
- Add indexes for frequently queried fields
- Write docstrings for models
- Document relationships clearly

### Templates (HTML)

- Use Bootstrap classes for consistency
- Include CSRF tokens in forms
- Validate on client and server side
- Keep JavaScript in separate files
- Comment complex template logic

### Forms (WTForms)

- Validate all user input
- Use custom validators for business logic
- Provide clear error messages
- Add help text for complex fields

## Testing

### Run Tests (When Available)

```bash
pytest tests/
pytest tests/test_auth.py  # Run specific test file
pytest tests/test_auth.py::test_user_registration  # Run specific test
```

### Writing Tests

Create tests in the `tests/` directory:

```python
# tests/test_auth.py
from app.models import User

def test_user_registration(client):
    """Test user registration with valid data"""
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert User.query.filter_by(username='testuser').first()
```

## Database Migrations

When you modify models, create a migration:

```bash
# Create migration
flask db migrate -m "Add profile table"

# Review the generated migration file in migrations/versions/

# Apply migration
flask db upgrade
```

**Important**: Always review auto-generated migrations — they sometimes need tweaks.

## Deployment Considerations

- Never commit `.env` (use `.env.example` as template)
- Test changes locally before pushing
- Ensure all dependencies are in `requirements.txt`
- Update documentation for public-facing changes
- Follow security best practices (password hashing, CSRF protection, etc.)

## Getting Help

- **Questions?** Check the README or docstrings first
- **Bug reports?** Create an issue with reproduction steps
- **Feature requests?** Discuss with the team first
- **Stuck?** Ask in PRs or create a discussion

## Good Practices

✅ Do:
- Create small, focused commits
- Write descriptive messages
- Test your changes locally
- Update documentation
- Follow the code style
- Communicate with team members
- Review others' code

❌ Don't:
- Push to `main` directly
- Commit sensitive data (.env, secrets, API keys)
- Make huge PRs without discussion
- Ignore failing CI checks
- Mix feature and refactor changes
- Leave commented-out code
- Commit merge conflicts

## Questions or Issues?

If you run into problems or have questions:
1. Check this guide and README
2. Check existing issues/PRs
3. Ask in the team chat or comment on issues
4. Create a new issue if needed

Happy coding! 🚀
