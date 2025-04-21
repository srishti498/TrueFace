# utils/auth.py
from flask_login import LoginManager, current_user
from functools import wraps
from flask import redirect, url_for, flash
from models.user import User

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader callback"""
    return User.get(user_id)

def admin_required(f):
    """Decorator to restrict access to admin users"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def password_complexity_check(password):
    """Check if password meets complexity requirements"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number"
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter"
    return True, ""

def generate_password_reset_token(user):
    """Generate a secure password reset token"""
    from itsdangerous import URLSafeTimedSerializer
    from app import app
    
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps({'user_id': user.id}, salt='password-reset-salt')

def verify_password_reset_token(token, expiration=3600):
    """Verify password reset token"""
    from itsdangerous import URLSafeTimedSerializer
    from app import app
    
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        user_id = serializer.loads(
            token,
            salt='password-reset-salt',
            max_age=expiration
        )['user_id']
    except:
        return None
    return User.get(user_id)

def log_failed_login_attempt(username, ip_address):
    """Log failed login attempts"""
    from datetime import datetime
    from models.db import get_db
    
    db = get_db()
    db.execute(
        "INSERT INTO login_attempts (username, ip_address, timestamp) VALUES (?, ?, ?)",
        (username, ip_address, datetime.utcnow())
    )
    db.commit()

def check_login_attempts(username, ip_address, max_attempts=5):
    """Check if too many failed login attempts"""
    from datetime import datetime, timedelta
    from models.db import get_db
    
    db = get_db()
    recent_attempts = db.execute(
        "SELECT COUNT(*) FROM login_attempts WHERE (username = ? OR ip_address = ?) AND timestamp > ?",
        (username, ip_address, datetime.utcnow() - timedelta(minutes=15))
    ).fetchone()[0]
    
    return recent_attempts >= max_attempts

def clear_login_attempts(username, ip_address):
    """Clear failed login attempts after successful login"""
    from models.db import get_db
    
    db = get_db()
    db.execute(
        "DELETE FROM login_attempts WHERE username = ? OR ip_address = ?",
        (username, ip_address)
    )
    db.commit()