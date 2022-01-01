from werkzeug.exceptions import BadRequest, NotFound

from db import db
from managers.authtoken import auth
from models import FoodAndDrinks
from models.orders import Order, Items


# https://www.guru99.com/json-tutorial-example.html#7
class CreateOrderManager:
    @staticmethod
    def get_all_orders():
        return Order.query.all()  # model.query.all()

    @staticmethod
    def create(data):
        items_list = data["items"]
        if not items_list:
            raise BadRequest("No items in order")

        # food_and_drinks_id = data["items"][0]["food_and_drinks_id"]
        # quantity = data["items"][0]["quantity"]

        del data["items"]
        order = Order(**data)
        db.session.add(order)
        db.session.flush()

        total_price = 0
        not_available = []
        for i in range(len(items_list)):
            food_and_drinks_id = items_list[i]["food_and_drinks_id"]
            f_d = FoodAndDrinks.query.filter_by(id=food_and_drinks_id).first()
            if not f_d or not f_d.is_available:
                not_available.append(f_d.title)
                continue
            quantity = items_list[i]["quantity"]
            price = f_d.price
            total_price += quantity * price

            # if food_and_drinks not available - break
            item_object = Items(
                order_id=order.id,
                food_and_drinks_id=food_and_drinks_id,
                quantity=quantity,
            )
            db.session.add(item_object)
            db.session.flush()

        # calculate total price
        order_query = Order.query.filter_by(id=order.id)
        order = order_query.first()
        order.total_price = total_price
        db.session.commit()
        return order, not_available

    @staticmethod
    def get(id_):  # by order_number????
        order_query = Order.query.filter_by(id=id_)
        order = order_query.first()
        if not order:
            raise NotFound("This order doesn't exist")

        user = auth.current_user()
        if not user.id == order.customer_id:
            raise NotFound("Customer doesn't have such order.")
        return order
