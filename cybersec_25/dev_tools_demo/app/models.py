from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    favorite_color = db.Column(db.String(64), nullable=True)  # persisted user preference
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def create_user(username: str, password: str, favorite_color: str | None = None):
        u = User(username=username, password_hash=generate_password_hash(password), favorite_color=favorite_color)
        db.session.add(u)
        db.session.commit()
        return u

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
