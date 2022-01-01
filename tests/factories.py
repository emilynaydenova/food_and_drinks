from db import db
from random import randint

import factory

from models.users import Admin
from models.enums import RoleEnum


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.commit()
        return object


class AdminFactory(BaseFactory):
    class Meta:
        model = Admin

    id = factory.Sequence(lambda n: n)
    full_name = factory.Faker("name")
    email = factory.Faker("email")
    phone = str(randint(100000, 200000))
    password = factory.Faker("password")
    role = RoleEnum.admin
