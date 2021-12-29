from datetime import datetime

from db import db
from models.enums import RoleEnum


class BaseUser(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True, unique=True)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<User {self.id} {self.full_name}>"


class Customer(BaseUser):
    __tablename__ = "customers"

    address = db.Column(db.String(100))
    points = db.Column(db.Integer, default=0)
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.customer, nullable=False)
    orders = db.relationship("Order", backref="customer", lazy="dynamic")
    # backref -> can use customer.(field of Orders)


class Staff(BaseUser):
    __tablename__ = "staff"

    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.staff, nullable=False)


class Admin(BaseUser):
    __tablename__ = "admins"

    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.admin, nullable=False)
