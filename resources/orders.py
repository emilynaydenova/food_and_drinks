from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from managers.authtoken import auth
from managers.orders import CreateOrderManager, ApprovementOrderManager
from models import RoleEnum
from schemas.request.orders import OrderRequestSchema
from schemas.response.orders import OrderResponseSchema
from utils.decorators import permission_required, validate_schema


class CreateOrder(Resource):
    @auth.login_required
    @permission_required([RoleEnum.staff])
    def get(self):
        if request.args:
            # get_all_orders by status (from ?query)
            args = dict(request.args)
            orders = CreateOrderManager.get_all_orders_by_status(args)  # list of objects
        else:
            orders = CreateOrderManager.get_all_orders()
            # Todo: get orders by date

        schema = OrderResponseSchema()
        return schema.dump(orders, many=True)

    # Create
    @auth.login_required
    @permission_required([RoleEnum.customer])
    @validate_schema(OrderRequestSchema)
    def post(self):
        data = request.get_json()

        order, not_available = CreateOrderManager.create(data)
        if not_available:
            message = f'There are unavailable food or drinks: {",".join(not_available)}'
            raise BadRequest(message)
        schema = OrderResponseSchema()
        return schema.dump(order), 201


class OrderDetails(Resource):
    # customer can see only his orders with their status
    @auth.login_required
    @permission_required([RoleEnum.customer])
    def get(self, id_):  # get order
        order = CreateOrderManager.get(id_)
        schema = OrderResponseSchema()
        return schema.dump(order), 200

    @auth.login_required
    @permission_required([RoleEnum.customer])
    @validate_schema(OrderRequestSchema)
    def put(self,id_):
        """
        change order's items while status is still "pending"
        """
        data = request.get_json()

        order, not_available = CreateOrderManager.update(data,id_)
        if not_available:
            message = f'There are unavailable food or drinks: {",".join(not_available)}'
            raise BadRequest(message)
        schema = OrderResponseSchema()
        return schema.dump(order), 201

class OrderApprovement(Resource):
    @auth.login_required
    @permission_required([RoleEnum.staff])
    @validate_schema(OrderRequestSchema)
    def put(self, id_):
        data = request.get_json()
        order = ApprovementOrderManager.update(data, id_)
        schema = OrderResponseSchema()
        return schema.dump(order), 201
