from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models.enums import StatusEnum


class OrderResponseSchema(Schema):
    id = fields.Integer(required=True)
    status = EnumField(StatusEnum, by_value=True)
    delivery = EnumField(StatusEnum, by_value=True)
    created_on = fields.DateTime(required=True)
    updated_on = fields.DateTime()
    total_price = fields.Float(required=True)
    customer_id = fields.Integer()
