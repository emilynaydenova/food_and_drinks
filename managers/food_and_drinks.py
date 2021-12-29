from werkzeug.exceptions import BadRequest

from db import db
from models import FoodAndDrinks, Category, CategoryEnum


# managers don't have state -> staticmethod
class FoodAndDrinksManager:
    @staticmethod
    def get_all_food_and_drinks():
        food_and_drinks = FoodAndDrinks.query.filter_by(is_available=True)
        return food_and_drinks

    @staticmethod
    def create(data):
        category_id = data["category_id"]
        category = Category.query.filter_by(id=category_id).first()
        if not category:
            raise BadRequest(f"Category does not exist")

        food_and_drinks = FoodAndDrinks(**data)
        db.session.add(food_and_drinks)
        db.session.flush()
        return food_and_drinks

    @staticmethod
    def get_all_food_and_drinks_by_category(args):
        if "category" not in args:
            return BadRequest("No query string with ?category received")

        category_value = args.get("category")
        try:
            category_name = CategoryEnum(category_value).name
        except Exception as ex:
            raise BadRequest(f"No such Category {category_value}.")

        category_found = Category.query.filter_by(title=category_name).first()

        if (not category_found) or (not category_found.is_active):
            raise BadRequest(f"No such active category.")

        foods_query = FoodAndDrinks.query.filter_by(category_id=category_found.id)
        foods = foods_query.all()
        if not foods:
            raise BadRequest("No foods and drinks in this category.")
        return foods

        # Update - can activate/deactivate a category

    @staticmethod
    def update(data, id_):
        food_query = FoodAndDrinks.query.filter_by(id=id_)
        if not food_query.first():
            raise BadRequest("Not such food or drink.")

        food_query.update(data)
        db.session.flush()

        updated_foods = FoodAndDrinks.query.filter_by(id=id_).first()
        db.session.flush()
        return updated_foods

    @staticmethod
    def delete(id_):
        food = FoodAndDrinks.query.filter_by(id=id_).first()
        if not food:
            raise BadRequest(f"There is not such food or drink")
        db.session.delete(food)
        db.session.flush()
        return food

    # ??????????
    @staticmethod
    def get(id_):
        foods = Category.query.filter_by(id=id_).first()
        if not foods:
            raise BadRequest(f"Category does not exist")
        return foods
