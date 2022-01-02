import json

from flask_testing import TestCase

from config import create_app
from db import db
from models import Customer, RoleEnum


class TestUsers(TestCase):

    def create_app(self):
        # Create Flask app with test configuration .
        self.headers = {"Content-Type": "application/json"}
        return create_app("config.TestApplicationConfig")

    def setUp(self):
        # before test
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        # after test
        db.session.remove()
        db.drop_all()

    def test_signup_customer(self):
        """
        Test if a customer is in database when register endpoint is hit.
        Assure that the role assign is a Customer role.
        """
        # Arrange
        url = "/users/customers/signup"

        data = {
            "email": "test@test.com",
            "password": "J@2345678",
            "full_name": "Test User",

        }

        customers = Customer.query.all()
        assert len(customers) == 0

        # Act
        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        # assert if customer is created and token is returned
        assert resp.status_code == 201
        assert "token" in resp.json

        customers = Customer.query.all()
        assert len(customers) == 1

        customer = Customer.query.filter_by(id=1).first()

        customer_created = {"id": customer.id, "email": customer.email, "full_name": customer.full_name,
                            "role": RoleEnum.customer}
        data.pop("password")
        assert customer_created == {
            "id": 1,
            "role": RoleEnum.customer,
            **data,
        }
