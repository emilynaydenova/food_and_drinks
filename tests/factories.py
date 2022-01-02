from db import db
from random import randint

import factory  # from factory_boy

from models.users import Admin, Customer, Staff
from models.enums import RoleEnum


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

    id = factory.Sequence(lambda n: n+1)
    full_name = factory.Faker("name")
    email = factory.Faker("email")
    phone = str(randint(1000000000, 2000000000))
    password = factory.Faker("password")
    is_active = True
    role = RoleEnum.admin


class CustomerFactory(BaseFactory):
    class Meta:
        model = Customer

    id = factory.Sequence(lambda n: n+1)
    full_name = factory.Faker("name")
    email = factory.Faker("email")
    phone = str(randint(1000000000, 2000000000))
    password = factory.Faker("password")
    is_active = True
    role = RoleEnum.customer


class StaffFactory(BaseFactory):
    class Meta:
        model = Staff

    id = factory.Sequence(lambda n: n+1)
    full_name = factory.Faker("name")
    email = factory.Faker("email")
    phone = str(randint(1000000000, 2000000000))
    password = factory.Faker("password")
    is_active = True
    role = RoleEnum.customer