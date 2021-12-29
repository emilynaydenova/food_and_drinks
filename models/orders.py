from datetime import datetime

from db import db
from models.enums import StatusEnum, DeliveryEnum


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.pending, nullable=False)
    delivery = db.Column(
        db.Enum(DeliveryEnum), default=DeliveryEnum.takeaway, nullable=False
    )
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))

    # order_number = db.Column(db.Integer)  # send email to customer
    total_price = db.Column(db.Float)


# many orders to many food_and_drinks
class Items(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    food_and_drinks_id = db.Column(
        db.Integer, db.ForeignKey("food_and_drinks.id"), nullable=False
    )
    quantity = db.Column(db.Integer)
    #  'food_and_drinks' property from db.relationship
