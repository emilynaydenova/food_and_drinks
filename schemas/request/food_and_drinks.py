from marshmallow import Schema, fields, validate


class FoodAndDrinksRequestSchema(Schema):

    title = fields.String(required=True, validate=validate.Length(max=50))
    description = fields.String(required=True)
    image = fields.String(required=True)
    image_extension = fields.String(required=True)

    price = fields.Float(required=True)  # be positive >0
    category_id = fields.Integer(required=True)
