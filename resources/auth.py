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


# (SignUpCustomer, "/users/customers/signup")
class SignUpCustomer(Resource):
    @validate_schema(SignUpCustomerRequestSchema)
    def post(self):
        user = CustomerManager.signup(request.get_json())
        token = AuthTokenManager.encode_token(user)
        return {"token": token}, 201


# must return dictionary or list of dictionaries, so Flask could serialize it in get_json


#  (SignInCustomer, "/users/customers/signin")
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


# (SignInAdmin, '/users/admin/signin')
class SignInAdmin(Resource):
    @validate_schema(SignInAdminSchema)
    def post(self):
        data = request.get_json()
        token = AdminManager.signin(data)
        return {"token": token}, status.HTTP_200_OK

    def put(self):
        pass

    # change password if not super admin


class HelloWorld(Resource):
    @staticmethod
    def get():
        return {"hello": "world"}


# https://restfulapi.net/http-methods/

#
# class CreateGuest(Resource):
#     @validate_schema(GuestRequestSchema)
#     def post(self):
#         pass
