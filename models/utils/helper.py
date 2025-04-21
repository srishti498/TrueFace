# utils/helpers.py
import os
import uuid
import datetime
from PIL import Image
from flask import current_app, request
from werkzeug.utils import secure_filename
import hashlib
import json
import re

# File Handling Helpers
def allowed_file(filename, allowed_extensions=None):
    """Check if file extension is allowed"""
    if allowed_extensions is None:
        allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_uploaded_file(file, folder='uploads'):
    """Save uploaded file with secure filename"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    file_path = os.path.join(folder, unique_name)
    file.save(file_path)
    return file_path

def resize_image(image_path, max_size=(800, 800), quality=85):
    """Resize image while maintaining aspect ratio"""
    with Image.open(image_path) as img:
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(image_path, quality=quality)
    return image_path

# Data Processing Helpers
def clean_input(data):
    """Sanitize user input"""
    if isinstance(data, str):
        return data.strip()
    elif isinstance(data, dict):
        return {k: clean_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_input(item) for item in data]
    return data

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_hash(data):
    """Generate SHA-256 hash of data"""
    if isinstance(data, dict):
        data = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()

# Date/Time Helpers
def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    """Format datetime object to string"""
    if value is None:
        return ""
    return value.strftime(format)

def parse_datetime(datetime_str, format='%Y-%m-%d %H:%M:%S'):
    """Parse string to datetime object"""
    try:
        return datetime.datetime.strptime(datetime_str, format)
    except (ValueError, TypeError):
        return None

def time_ago(dt):
    """Convert datetime to human-readable time ago string"""
    now = datetime.datetime.utcnow()
    diff = now - dt
    
    if diff.days > 365:
        return f"{diff.days // 365} years ago"
    if diff.days > 30:
        return f"{diff.days // 30} months ago"
    if diff.days > 0:
        return f"{diff.days} days ago"
    if diff.seconds > 3600:
        return f"{diff.seconds // 3600} hours ago"
    if diff.seconds > 60:
        return f"{diff.seconds // 60} minutes ago"
    return "just now"

# API Response Helpers
def api_response(data=None, message="", status="success", code=200):
    """Standard API response format"""
    return {
        "status": status,
        "code": code,
        "message": message,
        "data": data
    }, code

def paginate(query, page, per_page):
    """Paginate SQLAlchemy query"""
    return query.paginate(page=page, per_page=per_page, error_out=False)

# System Helpers
def get_client_ip():
    """Get client IP address from request"""
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']

def get_app_config(key, default=None):
    """Safely get Flask app config value"""
    try:
        return current_app.config[key]
    except:
        return default

# Face Verification Helpers
def extract_face_features(image_path):
    """Basic face feature extraction (placeholder"""