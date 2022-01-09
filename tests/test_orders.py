import json

from flask_testing import TestCase

from config import create_app
from db import db
from models import Order, Items
from tests.factories import CategoryFactory, CustomerFactory, FoodAndDrinksFactory, FoodAndDrinksFactorySecond
from tests.helpers import generate_token


class TestOrders(TestCase):
    """
    Test resources for creating orders.
    """

    def create_app(self):
        self.headers = {"Content-Type": "application/json"}
        return create_app("config.TestApplicationConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_order(self):
        """
            Integration Test - creating Order after hitting
            endpoint /orders/customers/order
        """

        # Create a test user
        customer = CustomerFactory()
        token = generate_token(customer)
        self.headers.update({"Authorization": f"Bearer {token}"})

        # Create a test category for testing food and drinks item
        category = CategoryFactory()
        foods1 = FoodAndDrinksFactory()
        foods2 = FoodAndDrinksFactorySecond()

        url = "/orders/customers/order"

        data = {
            "status": "pending",
            "delivery": "takeaway",
            "customer_id": customer.id,
            "items": [{"food_and_drinks_id": foods1.id,
                       "quantity": 2
                       },
                      {"food_and_drinks_id": foods2.id,
                       "quantity": 3
                       }]
        }

        orders = Order.query.all()
        assert len(orders) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        actual_resp = resp.json
        actual_resp.pop("created_on")
        actual_resp.pop("updated_on")

        orders = Order.query.all()
        assert len(orders) == 1
        items = Items.query.all()
        assert len(items) == 2

        expected_resp = {
            "id": 1,
            "total_price": 50.25,
            "status": "Pending",
            "delivery": "Takeaway",
            "customer_id": customer.id,
            "items": [{"food_and_drinks_id": 1,
                       "quantity": 2
                       },
                      {"food_and_drinks_id": 2,
                       "quantity": 3
                       }]
        }

        # assert if order is created correctly.
        assert resp.status_code == 201
        assert actual_resp == expected_resp
