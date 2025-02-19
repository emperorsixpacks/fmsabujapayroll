from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(
        db.String(10), nullable=False, default="employee"
    )  # "admin" or "employee"

    # Explicit Relationship
    payslips = db.relationship(
        "Payslip",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def is_admin(self):
        return self.role == "admin"


class Payslip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Explicit Relationship
    user = db.relationship("User", back_populates="payslips")
