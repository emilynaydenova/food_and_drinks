from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from models.enums import StatusEnum


class ItemsResponseSchema(Schema):
    food_and_drinks_id = fields.Integer()
    quantity = fields.Integer()


class OrderResponseSchema(Schema):
    id = fields.Integer(required=True)
    status = EnumField(StatusEnum, by_value=True)
    delivery = EnumField(StatusEnum, by_value=True)
    created_on = fields.DateTime(required=True)
    updated_on = fields.DateTime()
    total_price = fields.Float(required=True,validate=validate.Range(min=0))
    customer_id = fields.Integer()
    items = fields.Nested(ItemsResponseSchema, many=True)