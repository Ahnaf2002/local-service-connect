import os
from app import create_app, db
from app.models import User, Order, Payment
from dotenv import load_dotenv

load_dotenv()

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Add objects to shell context"""
    return {
        'db': db,
        'User': User,
        'Order': Order,
        'Payment': Payment,
    }

@app.route('/')
def index():
    """Home page route"""
    from flask import render_template
    return render_template('index.html')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', True)
    )
