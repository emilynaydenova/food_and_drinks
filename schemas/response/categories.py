from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models.enums import CategoryEnum


class CategoryResponseSchema(Schema):
    id = fields.Integer(required=True)
    title = EnumField(
        CategoryEnum, by_value=True
    )  # by_value returns Value of enum field
    image_url = fields.URL(required=True)
    is_active = fields.Boolean(required=True)
