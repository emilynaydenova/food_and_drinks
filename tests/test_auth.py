import json

#  inherits unittest.TestCase
from flask_testing import TestCase

from config import create_app
from db import db
from tests.factories import AdminFactory, CustomerFactory, StaffFactory
from tests.helpers import generate_token


class TestAuthenticationAuthorization(TestCase):
    def create_app(self):
        # Create Flask app with test configuration .
        return create_app("config.TestApplicationConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_authentication_missing_auth_header_raises(self):
        # tests decorator @auth.login_required

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
            ("/orders/approvement/1", "PUT"),
            ("/admin/create-staff", "POST"),
            ("/admin/create-admin", "POST"),
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

            assert resp.status_code == 401  # Unauthorized,expired
            assert resp.json == {
                "message": "Invalid or missing token. Please log in again."
            }

    def test_authorization_endpoints_admin_access_raises(self):
        # tests decorator @permission_required([RoleEnum.admin])

        # Create Admin, create token for it and test all
        # Admin endpoints if they have permission for this resource

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

        admin = AdminFactory()
        token = generate_token(admin)
        headers = {"Authorization": f"Bearer {token}"}

        for url, method in url_methods:
            if method == "GET":
                resp = self.client.get(url, headers=headers)
            elif method == "DELETE":
                resp = self.client.delete(url, headers=headers)
            elif method == "POST":
                resp = self.client.post(url, data=json.dumps({}), headers=headers)
            elif method == "PUT":
                resp = self.client.put(url, data=json.dumps({}), headers=headers)

            assert resp.status_code != 403  # if not permission -> 403 -> Forbidden
            assert resp.json != {"message": "You don't have access to this resource."}

    def test_if_only_customer_can_create_an_order(self):
        # tests decorator @permission_required([RoleEnum.customer])
        url_methods = [
            ("/orders/customers/order", "POST"),
            ("/orders/details/1", "PUT"),
        ]

        admin = AdminFactory()
        token = generate_token(admin)
        headers = {"Authorization": f"Bearer {token}"}

        for url, method in url_methods:
            if method == "POST":
                resp = self.client.post(url, data=json.dumps({}), headers=headers)
            elif method == "PUT":
                resp = self.client.put(url, data=json.dumps({}), headers=headers)

            assert resp.status_code == 403
            assert resp.json == {"message": "You don't have access to this resource."}

        staff = StaffFactory()
        token = generate_token(staff)
        headers = {"Authorization": f"Bearer {token}"}

        for url, method in url_methods:
            if method == "POST":
                resp = self.client.post(url, data=json.dumps({}), headers=headers)
            elif method == "PUT":
                resp = self.client.put(url, data=json.dumps({}), headers=headers)

            assert resp.status_code == 403
            assert resp.json == {"message": "You don't have access to this resource."}

        customer = CustomerFactory()
        token = generate_token(customer)
        headers = {"Authorization": f"Bearer {token}"}

        for url, method in url_methods:
            if method == "POST":
                resp = self.client.post(url, data=json.dumps({}), headers=headers)
            elif method == "PUT":
                resp = self.client.put(url, data=json.dumps({}), headers=headers)

        assert resp.status_code != 403
        assert resp.json != {"message": "You don't have access to this resource."}

