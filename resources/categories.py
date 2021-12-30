from flask import request
from flask_restful import Resource

from managers.authtoken import auth
from managers.categories import CategoryManager
from models import RoleEnum
from schemas.request.categories import CategoryRequestSchema
from schemas.response.categories import CategoryResponseSchema
from utils.decorators import validate_schema, permission_required


class CreateCategory(Resource):
    # all categories
    @auth.login_required
    @permission_required([RoleEnum.admin])
    def get(self):
        categories = CategoryManager.get_all_categories()
        schema = CategoryResponseSchema()
        return schema.dump(categories, many=True)

    # Create
    @auth.login_required
    @permission_required([RoleEnum.admin])
    @validate_schema(CategoryRequestSchema)
    def post(self):
        data = request.get_json()
        category = CategoryManager.create(data)
        schema = CategoryResponseSchema()
        return schema.dump(category), 201


class CategoryDetails(Resource):
    @auth.login_required
    @permission_required([RoleEnum.admin])
    def get(self, id_):
        category = CategoryManager.get(id_)
        schema = CategoryResponseSchema()
        return schema.dump(category)

    # Update
    @auth.login_required
    @permission_required([RoleEnum.admin])
    @validate_schema(CategoryRequestSchema)
    def put(self, id_):
        data = request.get_json()
        updated_category = CategoryManager.update(data, id_)
        schema = CategoryResponseSchema()
        return schema.dump(updated_category)

    # Delete
    @auth.login_required
    @permission_required([RoleEnum.admin])
    def delete(self, id_):
        CategoryManager.delete(id_)
        return {"message": "Success"}, 204
