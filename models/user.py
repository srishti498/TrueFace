# models/user.py
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from models.db import get_db

class User(UserMixin):
    def __init__(self, id, username, password_hash, is_admin=False):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin

    def verify_password(self, password):
        """Check if provided password matches the stored hash"""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def create(username, password, is_admin=False):
        """Create a new user"""
        db = get_db()
        password_hash = generate_password_hash(password)
        try:
            db.execute(
                "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
                (username, password_hash, int(is_admin))
            )
            db.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    @staticmethod
    def get(user_id):
        """Get user by ID"""
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None
        return User(id=user['id'], 
                   username=user['username'], 
                   password_hash=user['password_hash'],
                   is_admin=bool(user['is_admin']))

    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        if not user:
            return None
        return User(id=user['id'], 
                   username=user['username'], 
                   password_hash=user['password_hash'],
                   is_admin=bool(user['is_admin']))

    @staticmethod
    def update(user_id, username=None, password=None, is_admin=None):
        """Update user details"""
        db = get_db()
        updates = []
        params = []
        
        if username is not None:
            updates.append("username = ?")
            params.append(username)
        if password is not None:
            updates.append("password_hash = ?")
            params.append(generate_password_hash(password))
        if is_admin is not None:
            updates.append("is_admin = ?")
            params.append(int(is_admin))
            
        if not updates:
            return False
            
        params.append(user_id)
        query = "UPDATE users SET " + ", ".join(updates) + " WHERE id = ?"
        
        try:
            db.execute(query, params)
            db.commit()
            return True
        except sqlite3.Error:
            return False

    @staticmethod
    def delete(user_id):
        """Delete a user"""
        db = get_db()
        try:
            db.execute("DELETE FROM users WHERE id = ?", (user_id,))
            db.commit()
            return True
        except sqlite3.Error:
            return False

    @staticmethod
    def get_all():
        """Get all users"""
        db = get_db()
        users = db.execute("SELECT * FROM users ORDER BY username").fetchall()
        return [User(id=u['id'], 
                username=u['username'], 
                password_hash=u['password_hash'],
                is_admin=bool(u['is_admin'])) for u in users]

    def to_dict(self):
        """Return user data as dictionary (without sensitive info)"""
        return {
            'id': self.id,
            'username': self.username,
            'is_admin': self.is_admin
        }