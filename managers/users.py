from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.authtoken import AuthTokenManager
from models import Customer, Admin, Staff


class CustomerManager:
    @staticmethod
    def signup(data):
        # check for unique email address
        if Customer.query.filter_by(email=data["email"]).first():
            raise BadRequest("User with this email already exists")

        data["password"] = generate_password_hash(
            data["password"], method="sha256", salt_length=5
        )
        customer = Customer(**data)  # new instance of Customer
        # Todo: try - except for UniqueViolationError
        db.session.add(customer)
        db.session.commit()
        return customer

    @staticmethod
    def signin(data):
        customer = Customer.query.filter_by(email=data["email"]).first()
        if customer and check_password_hash(customer.password, data["password"]):
            return customer
        else:
            raise BadRequest("Invalid email or password")


class StaffManager:
    @staticmethod
    def create(data):
        if Staff.query.filter_by(email=data["email"]).first():
            raise BadRequest("Staff with this email already exists")

        data["password"] = generate_password_hash(
            data["password"], method="sha256", salt_length=5
        )
        staff = Staff(**data)
        # Todo: try - except for UniqueViolationError
        db.session.add(staff)
        db.session.commit()
        return staff

    @staticmethod
    def signin(data):
        try:
            staff = Staff.query.filter_by(email=data["email"]).first()
            if staff and check_password_hash(staff.password, data["password"]):
                return AuthTokenManager.encode_token(staff)
            raise Exception
        except Exception:
            raise BadRequest("Invalid email or password")

class AdminManager:
    @staticmethod
    def create(data):
        if Admin.query.filter_by(email=data["email"]).first():
            raise BadRequest("Admin with this email already exists")

        data["password"] = generate_password_hash(
            data["password"], method="sha256", salt_length=5
        )
        admin = Admin(**data)
        # Todo: try - except for UniqueViolationError
        db.session.add(admin)
        db.session.commit()
        return admin

    @staticmethod
    def signin(data):
        """
        Checks the email and password (hashes the plain password)
        :param data: dict -> email, password
        :return: token
        """
        try:
            admin = Admin.query.filter_by(email=data["email"]).first()
            if admin and check_password_hash(admin.password, data["password"]):
                return AuthTokenManager.encode_token(admin)
            raise Exception
        except Exception:
            raise BadRequest("Invalid email or password")


