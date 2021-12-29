from marshmallow import Schema, fields


class FoodAndDrinksResponseSchema(Schema):

    id = fields.Integer(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    image_url = fields.URL(required=True)
    price = fields.Float(required=True)
    category_id = fields.Integer(required=True)
    is_available = fields.Boolean()
    likes = fields.Integer()
