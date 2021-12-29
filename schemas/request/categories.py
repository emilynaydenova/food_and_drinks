from marshmallow import Schema, fields

from utils.validators import validate_category


class CategoryRequestSchema(Schema):
    title = fields.String(required=True, validate=validate_category)
    image = fields.String(required=True)
    image_extension = fields.String(required=True)
    is_active = fields.Boolean(required=True)
