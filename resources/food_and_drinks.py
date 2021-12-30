from flask import request
from flask_restful import Resource

from managers.authtoken import auth
from managers.food_and_drinks import FoodAndDrinksManager
from models import RoleEnum
from schemas.request.food_and_drinks import FoodAndDrinksRequestSchema
from schemas.response.food_and_drinks import FoodAndDrinksResponseSchema
from utils.decorators import permission_required, validate_schema


# '/orders/food-and-drinks'
class CreateFoodAndDrinks(Resource):
    # all food and drinks
    @auth.login_required
    @permission_required([RoleEnum.staff, RoleEnum.admin])
    def get(self):
        food_and_drinks = FoodAndDrinksManager.get_all_food_and_drinks()
        schema = FoodAndDrinksResponseSchema()
        return schema.dump(food_and_drinks, many=True)

    # Create
    @auth.login_required
    @permission_required([RoleEnum.staff, RoleEnum.admin])
    @validate_schema(FoodAndDrinksRequestSchema)
    def post(self):
        data = request.get_json()
        food_and_drinks = FoodAndDrinksManager.create(data)
        schema = FoodAndDrinksResponseSchema()
        return schema.dump(food_and_drinks), 201


# /orders/food-and-drinks/<int:id>'
class FoodAndDrinksDetails(Resource):
    @auth.login_required
    @permission_required([RoleEnum.staff, RoleEnum.admin])
    def get(self, id_):
        category = FoodAndDrinksManager.get(id_)
        schema = FoodAndDrinksResponseSchema()
        return schema.dump(category)

    # Update
    @auth.login_required
    @permission_required([RoleEnum.staff, RoleEnum.admin])
    @validate_schema(FoodAndDrinksRequestSchema)
    def put(self, id_):
        data = request.get_json()
        updated_food_and_drinks_item = FoodAndDrinksManager.update(data, id_)
        schema = FoodAndDrinksResponseSchema()
        return schema.dump(updated_food_and_drinks_item)

    # Delete
    @auth.login_required
    @permission_required([RoleEnum.staff, RoleEnum.admin])
    def delete(self, id_):
        FoodAndDrinksManager.delete(id_)
        return {"message": "Success"}, 204
