from werkzeug.exceptions import BadRequest, NotFound

from db import db
from managers.authtoken import auth
from models import FoodAndDrinks, StatusEnum
from models.orders import Order, Items


def find_order(id_):
    order = Order.query.filter_by(id=id_).first()
    if not order:
        raise BadRequest(f"Order does not exist")
    return order


class CreateOrderManager:
    @staticmethod
    def get_all_orders():
        return Order.query.all()

    @staticmethod
    def get_all_orders_by_status(args):
        args = {k.lower(): v.lower() for k, v in args.items()}
        if "status" not in args:
            return BadRequest("No query string with ?status received")

        status_value = args.get("status")

        for k, v in StatusEnum.__members__.items():
            if k == status_value.lower():
                status_name = v
                break
        else:
            raise BadRequest("Not such status name.")

        orders = Order.query.filter_by(status=status_name)

        if not orders:
            raise BadRequest(f"No orders with this status.")
        return orders

    @staticmethod
    def create(data):
        items_list = data["items"]
        if not items_list:
            raise BadRequest("No items in order")

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
    def update(data, id_):
        if data['status'] != "pending":
            raise BadRequest("Order have been processed yet.")

        old_items = Items.query.filter_by(order_id=id_).all()
        try:
            for el in old_items:
                db.session.delete(el)
                db.session.flush()
        except Exception as e:
            raise BadRequest(f"Can't delete these food and drinks items.{e}")

        items_list = data["items"]
        if not items_list:
            raise BadRequest("No items in order")

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
            #
            # if food_and_drinks not available - break
            item_object = Items(
                order_id=id_,
                food_and_drinks_id=food_and_drinks_id,
                quantity=quantity,
            )
            db.session.add(item_object)
            db.session.flush()

        # calculate total price
        order = find_order(id_)
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


class ApprovementOrderManager:
    """
   Order's status can be changed under the following conditions:
       if old status is "Pending" -> new status can be "Approved" or "Rejected"
       if old status is "Approved" -> new status can be "Rejected or "Delivered"
       if old status is "Rejected" or "Delivered" -> status can't be changed
   """

    @staticmethod
    def update(data, id_):
        order = find_order(id_)
        old_status = order.status.name
        new_status = data["status"].lower()
        if (old_status == "pending" and new_status in ["approved", "rejected"]) or \
                (old_status == "approved" and new_status in ["rejected", "delivered"]):
            order.status = StatusEnum[new_status]
            db.session.commit()
        else:
            raise BadRequest("Order's status can't be changed.")
        order = find_order(id_)
        return order
