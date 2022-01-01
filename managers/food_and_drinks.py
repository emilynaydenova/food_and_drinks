from werkzeug.exceptions import BadRequest

from db import db
from managers.categories import s3_image_upload
from models import FoodAndDrinks, Category, CategoryEnum
from services.aws.s3 import S3Service

s3 = S3Service()


def find_food_and_drinks_item(id_):
    food_and_drinks_item = FoodAndDrinks.query.filter_by(id=id_).first()
    if not food_and_drinks_item:
        raise BadRequest("Not such food or drink.")
    return food_and_drinks_item


# managers don't have state -> staticmethod
class FoodAndDrinksManager:

    # Read from staff and admins
    @staticmethod
    def get_all_food_and_drinks():
        food_and_drinks = FoodAndDrinks.query.all()
        return food_and_drinks

    # Create
    @staticmethod
    def create(f_data):
        f_data = s3_image_upload(f_data)

        food_and_drinks = FoodAndDrinks(**f_data)
        db.session.add(food_and_drinks)
        db.session.commit()
        return food_and_drinks

    # Update - can make dish available/not available
    @staticmethod
    def update(f_data, id_):
        # check if item exists
        food_and_drinks_item = find_food_and_drinks_item(id_)
        s3.delete_image(food_and_drinks_item.image_url)

        f_data = s3_image_upload(f_data)
        FoodAndDrinks.query.filter_by(id=id_).update(f_data)
        db.session.commit()

        updated_foods = FoodAndDrinks.query.filter_by(id=id_).first()
        return updated_foods

    # Delete
    @staticmethod
    def delete(id_):
        food = find_food_and_drinks_item(id_)
        try:
            s3.delete_image(food.image_url)
            db.session.delete(food)
            db.session.commit()
        except Exception as e:
            raise BadRequest("Can't delete this food and drinks item.")
        return food

    @staticmethod
    def get(id_):
        food = find_food_and_drinks_item(id_)
        return food

    @staticmethod
    def get_all_food_and_drinks_by_category(args):
        args = {k.lower(): v.lower() for k, v in args.items()}
        if "category" not in args:
            return BadRequest("No query string with ?category received")

        category_value = args.get("category")

        for k, v in CategoryEnum.__members__.items():
            if k == category_value.lower():
                category_name = v
                break
        else:
            raise BadRequest("Not such category name.")

        category_found = Category.query.filter_by(title=category_name).first()

        if (not category_found) or (not category_found.is_active):
            raise BadRequest(f"No such active category.")

        # show only available foods for this category
        foods = FoodAndDrinks.query.filter_by(category_id=category_found.id, is_available=True)

        if not foods:
            raise BadRequest("No foods and drinks in this category.")
        return foods
