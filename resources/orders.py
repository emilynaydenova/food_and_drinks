from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from managers.authtoken import auth
from managers.orders import CreateOrderManager
from models import RoleEnum
from schemas.request.orders import OrderRequestSchema
from schemas.response.orders import OrderResponseSchema
from utils.decorators import permission_required, validate_schema


class CreateOrder(Resource):
    #
    # # get_all_orders by status (from ?query)
    # @auth.login_required
    # @permission_required([RoleEnum.staff,RoleEnum.admin])
    # def get(self):
    #     # TODO add logic for different roles
    #     orders = OrderManager.get_all_orders()
    #     schemas = ComplaintCreateResponseSchema()
    #     return schemas.dump(orders, many=True)  # list of json objects

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
    @permission_required([RoleEnum.staff,RoleEnum.customer])
    def put(self, id_):  # update order - change status or change items
        pass

