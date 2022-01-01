#  inherits unittest.TestCase
import json

from flask_testing import TestCase

from config import create_app
from db import db
from tests.base import generate_token
from tests.factories import AdminFactory


class TestAuthenticationAuthorization(TestCase):

    def create_app(self):
        # Create Flask app with test configuration .
        return create_app("config.TestApplicationConfig")

    def setUp(self):
        # before test
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        # after test
        db.session.remove()
        db.drop_all()

    def test_authentication_missing_auth_header_raises(self):
        # tests    @auth.login_required

        # Arrange
        url_methods = [

            ("/orders/categories", "GET"),
            ("/orders/categories", "POST"),
            ("/orders/categories/1", "PUT"),
            ("/orders/categories/1", "DELETE"),

            ("/orders/food-and-drinks", "GET"),
            ("/orders/food-and-drinks", "POST"),
            ("/orders/food-and-drinks/1", "PUT"),
            ("/orders/food-and-drinks/1", "DELETE"),

            ("/orders/customers/order", "POST"),
            ("/orders/details/1", "GET"),
            ("/orders/details/1", "PUT"),

            ("/admin/create-staff", "POST"),
            ("/admin/create-admin", "POST"),
        ]

        # Act
        for url, method in url_methods:
            if method == "GET":
                resp = self.client.get(url)
            elif method == "POST":
                resp = self.client.post(url, data=json.dumps({}))
            elif method == "PUT":
                resp = self.client.put(url, data=json.dumps({}))
            elif method == "DELETE":
                resp = self.client.delete(url)

            # Assert
            assert resp.status_code == 401  # Unauthorized,expired
            assert resp.json == {"message": "Invalid or missing token. Please log in again."}

    def test_authorization_endpoints_admin_access_raises(self):
        # Create complainer, create token for it and test all
        # ADMIN endpoints with complainer token -
        # they should return
        url_methods = [
            ("/admin/create-staff", "POST"),
            ("/admin/create-admin", "POST"),

            ("/orders/categories", "POST"),
            ("/orders/categories", "GET"),
            ("/orders/categories/1", "GET"),
            ("/orders/categories/1", "PUT"),
            ("/orders/categories/1", "DELETE"),

            ("/orders/food-and-drinks", "GET"),
            ("/orders/food-and-drinks", "POST"),
            ("/orders/food-and-drinks/1", "PUT"),
            ("/orders/food-and-drinks/1", "DELETE"),
        ]

        for url, method in url_methods:
            if method == "GET":
                resp = self.client.get(url)
            elif method == "POST":
                resp = self.client.post(url, data=json.dumps({}))
            elif method == "PUT":
                resp = self.client.put(url, data=json.dumps({}))
            elif method == "DELETE":
                resp = self.client.delete(url)

            admin = AdminFactory()
            token = generate_token(admin)
            headers = {"Authorization": f"Bearer {token}"}
            if method == "POST":
                resp = self.client.post(url, data=json.dumps({}), headers=headers)
            elif method == "DELETE":
                resp = self.client.delete(url, headers=headers)
            expected_message = {'message': 'You do not have the rights to access this resource'}
            self.assert_403(resp, expected_message)

    def test_first_admin_creation(self):
        pass

    def test_admin_cant_create_order(self):
        pass
