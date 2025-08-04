from datetime import datetime
from app import db


class User(db.Model):
    """
    User model representing employees in the system.

    Attributes:
        id (int): Primary key, auto-incrementing user ID
        name (str): Full name of the user
        email (str): Unique email address
        department (str): Department/team the user belongs to
        created_at (datetime): Timestamp when record was created
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    department = db.Column(db.String(50), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self, name, email, department):
        self.name = name
        self.email = email
        self.department = department

    def __repr__(self):
        """String representation of the User object."""
        return f"<User {self.id}: {self.name} ({self.email})>"

    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "created_at": self.created_at,
        }
        return data

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_department(cls, department):
        return cls.query.filter_by(department=department).all()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
