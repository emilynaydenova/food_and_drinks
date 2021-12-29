from decouple import config
from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash

from db import db
from managers.authtoken import auth
from managers.users import StaffManager, AdminManager
from models import Admin
from models.enums import RoleEnum
from schemas.request.users import CreateStaffSchema, CreateAdminSchema
from utils.decorators import permission_required, validate_schema


class CreateStaff(Resource):
    @auth.login_required
    @permission_required([RoleEnum.admin])
    @validate_schema(CreateStaffSchema)
    def post(self):
        data = request.get_json()
        StaffManager.create(data)
        return {"message": "Staff member account was created"}, 201


class CreateAdmin(Resource):
    @auth.login_required
    @permission_required([RoleEnum.admin])
    @validate_schema(CreateAdminSchema)
    def post(self):
        data = request.get_json()
        AdminManager.create(data)
        return {"message": "Admin account was created"}, 201


class CreateFirstAdmin(Resource):
    @staticmethod
    def post():
        if Admin.query.filter_by(email=config("FA_EMAIL")).first():
            raise BadRequest("First Admin had been created.")

        email = config("FA_EMAIL")
        password = config("FA_PASSWORD")
        admin = Admin(
            full_name="First Admin",
            email=email,
            password=generate_password_hash(password, method="sha256", salt_length=5),
            role=RoleEnum.admin,
        )
        db.session.add(admin)
        db.session.commit()
        return {"message": "First Admin was created"}, 201


class DisableUsers(Resource):
    pass
