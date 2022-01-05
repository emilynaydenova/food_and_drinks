import json
import os
from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from constants import TEMP_FILE_FOLDER
from db import db
from models import FoodAndDrinks
from services.aws.s3 import S3Service
from tests.factories import CategoryFactory, StaffFactory
from tests.helpers import encoded_image, generate_token, mock_uuid


class TestFoodAndDrinks(TestCase):
    """
    Test resources for food and drinks. AWS S3 service is mocked
    for images in food and drinks.
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

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(S3Service, "upload_image", return_value="some-test.url")
    def test_create_food_and_drinks_items(self, s3_mock):
        """
            Integration Test - creating Food and Drinks item after hitting
            endpoint /orders/food-and-drinks
        """

        # Create a test user
        staff = StaffFactory()
        token = generate_token(staff)
        self.headers.update({"Authorization": f"Bearer {token}"})

        # Create a test category for testing food and drinks item
        category = CategoryFactory()

        url = "/orders/food-and-drinks"

        data = {
            "title": "Test food and drinks item",
            "description": "Some description",
            "image": encoded_image,
            "image_extension": "png",
            "price": 10.05,
            "category_id": 1,
            "is_available": True
        }

        foods = FoodAndDrinks.query.all()
        assert len(foods) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)
        actual_resp = resp.json

        foods = FoodAndDrinks.query.all()
        assert len(foods) == 1

        data.pop("image")
        extension = data.pop("image_extension")

        expected_resp = {
            "id": 1,
            "image_url": "some-test.url",
            **data,
        }

        # assert if food and drinks item is created correctly.
        assert resp.status_code == 201
        assert actual_resp == expected_resp

        # test if s3.upload_image(path,image_name) is mocked and working
        image_name = f"{mock_uuid()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, image_name)
        s3_mock.assert_called_once_with(path, image_name)




    # def test_create_category_invalid_input_fields_raises(self):
    #     """
    #     Test if a required field is not provided
    #     """
    #
    #     url = "/orders/categories"
    #     data = {
    #         "title": CategoryEnum.salad.value,
    #         "image": encoded_image,
    #         "image_extension": "png",
    #         "is_active": True,
    #     }
    #     admin = AdminFactory()
    #     token = generate_token(admin)
    #     self.headers.update({"Authorization": f"Bearer {token}"})
    #
    #     categories = Category.query.all()
    #     assert len(categories) == 0
    #
    #     for key in data:
    #         copy_data = data.copy()
    #         copy_data.pop(key)
    #         resp = self.client.post(
    #             url, data=json.dumps(copy_data), headers=self.headers
    #         )
    #
    #         message = resp.json["message"]
    #         expected_message = f"Invalid data fields - {key}"
    #
    #         assert resp.status_code == 400
    #         assert message == expected_message
    #
    #     categories = Category.query.all()
    #     assert len(categories) == 0
    #
    # def test_create_category_invalid_title_field_raises(self):
    #     """
    #     Test if a title field is not from CategoryEnum
    #     """
    #
    #     url = "/orders/categories"
    #     data = {
    #         "title": "Test",
    #         "image": encoded_image,
    #         "image_extension": "png",
    #         "is_active": True,
    #     }
    #
    #     admin = AdminFactory()
    #     token = generate_token(admin)
    #     self.headers.update({"Authorization": f"Bearer {token}"})
    #
    #     categories = Category.query.all()
    #     assert len(categories) == 0
    #
    #     resp = self.client.post(url, data=json.dumps(data), headers=self.headers)
    #
    #     message = resp.json["message"]
    #     expected_message = f"No such category name."
    #
    #     assert resp.status_code == 400
    #     assert message == expected_message
    #
    #     categories = Category.query.all()
    #     assert len(categories) == 0
