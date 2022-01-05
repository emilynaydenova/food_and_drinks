# Authentication

from flask import request
from flask_api import status
from flask_restful import Resource

from managers.authtoken import AuthTokenManager
from managers.users import CustomerManager, AdminManager, StaffManager
from schemas.request.users import (
    SignUpCustomerRequestSchema,
    SignInAdminSchema,
    SignInCustomerRequestSchema, SignInStaffSchema,
)
from utils.decorators import validate_schema


class SignUpCustomer(Resource):
    @validate_schema(SignUpCustomerRequestSchema)
    def post(self):
        user = CustomerManager.signup(request.get_json())
        token = AuthTokenManager.encode_token(user)
        return {"token": token}, 201


class SignInCustomer(Resource):
    @validate_schema(SignInCustomerRequestSchema)
    def post(self):
        user = CustomerManager.signin(request.get_json())
        token = AuthTokenManager.encode_token(user)
        return {"token": token}, 200

    def put(self):
        pass

    # change password,address,phone


class SignInStaff(Resource):
    @validate_schema(SignInStaffSchema)
    def post(self):
        data = request.get_json()
        token = StaffManager.signin(data)
        return {"token": token}, status.HTTP_200_OK

    def put(self):
        pass

    # change password,address,phone


class SignInAdmin(Resource):
    @validate_schema(SignInAdminSchema)
    def post(self):
        data = request.get_json()
        token = AdminManager.signin(data)
        return {"token": token}, status.HTTP_200_OK

    def put(self):
        pass

    # change password if not first admin


class HelloWorld(Resource):
    @staticmethod
    def get():
        return {"hello": "world"}

