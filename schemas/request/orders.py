from marshmallow import Schema, fields


class ItemsRequestSchema(Schema):
    food_and_drinks_id = fields.Integer()
    quantity = fields.Integer()


class OrderRequestSchema(Schema):
    status = fields.String(required=True)
    delivery = fields.String(required=True)
    customer_id = fields.Integer(required=True)
    items = fields.Nested(ItemsRequestSchema, many=True)
