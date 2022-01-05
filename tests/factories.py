from random import randint

import factory  # from factory_boy

from db import db
from models.categories import Category
from models.food_and_drinks import FoodAndDrinks
from models.enums import RoleEnum, CategoryEnum
from models.users import Admin, Customer, Staff


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        # override the method, so add Factory object's features
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.commit()
        return object


class AdminFactory(BaseFactory):
    class Meta:
        model = Admin

    id = factory.Sequence(lambda n: n + 1)
    full_name = factory.Faker("name")
    email = factory.Faker("email")
    phone = str(randint(1000000000, 2000000000))
    password = factory.Faker("password")
    is_active = True
    role = RoleEnum.admin


class CustomerFactory(BaseFactory):
    class Meta:
        model = Customer

    id = factory.Sequence(lambda n: n + 1)
    full_name = factory.Faker("name")
    email = factory.Faker("email")
    phone = str(randint(1000000000, 2000000000))
    password = factory.Faker("password")
    is_active = True
    role = RoleEnum.customer


class StaffFactory(BaseFactory):
    class Meta:
        model = Staff

    id = factory.Sequence(lambda n: n + 1)
    full_name = factory.Faker("name")
    email = factory.Faker("email")
    phone = str(randint(1000000000, 2000000000))
    password = factory.Faker("password")
    is_active = True
    role = RoleEnum.staff


class CategoryFactory(BaseFactory):
    class Meta:
        model = Category

    id = 1
    title = CategoryEnum.salad
    image_url = "category-test.url"
    is_active = True


class FoodAndDrinksFactory(BaseFactory):
    class Meta:
        model = FoodAndDrinks

    id = 1
    title = "Test title 1"
    description = "Some description"
    image_url = "food-and-drinks.url"
    price = 10.05
    category_id = 1
    is_available = True


class FoodAndDrinksFactorySecond(BaseFactory):
    class Meta:
        model = FoodAndDrinks

    id = 2
    title = "Test title 2"
    description = "Some description"
    image_url = "food-and-drinks.url"
    price = 10.05
    category_id = 1
    is_available = True