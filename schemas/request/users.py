# Schemas for validation

from marshmallow import Schema, fields, validate

from utils.validators import validate_password


class BaseUserSchema(Schema):
    email = fields.Email(required=True)

    password = fields.String(
        required=True,
        validate=validate.And(validate.Length(min=8, max=120), validate_password),
    )


class SignUpCustomerRequestSchema(BaseUserSchema):
    full_name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=255),
    )


class SignInCustomerRequestSchema(BaseUserSchema):
    pass


class CreateStaffSchema(BaseUserSchema):
    full_name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=255),
    )


class CreateAdminSchema(BaseUserSchema):
    full_name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=255),
    )


class SignInAdminSchema(BaseUserSchema):
    pass


class SignInStaffSchema(BaseUserSchema):
    pass
