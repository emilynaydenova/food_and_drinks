import json
import os
from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from constants import TEMP_FILE_FOLDER
from db import db
from models import Category, CategoryEnum
from services.aws.s3 import S3Service
from tests.factories import AdminFactory
from tests.helpers import encoded_image, generate_token, mock_uuid


class TestCategories(TestCase):
    """
    Test resources for categories. AWS S3 service is mocked
    for images in categories.
    """

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

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(S3Service, "upload_image", return_value="some-test.url")
    # instead of method upload_image in S3Service to return url value
    def test_create_category(self, s3_mock):
        url = "/orders/categories"
        data = {
            "title": CategoryEnum.salad.value,
            "image": encoded_image,
            "image_extension": "png",
            "is_active": True
        }
        admin = AdminFactory()
        token = generate_token(admin)
        self.headers.update({"Authorization": f"Bearer {token}"})

        categories = Category.query.all()
        assert len(categories) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        categories = Category.query.all()
        assert len(categories) == 1

        data.pop("image")
        extension = data.pop("image_extension")

        expected_resp = {
            "id": 1,
            "image_url": "some-test.url",
            **data,
        }
        actual_resp = resp.json

        assert resp.status_code == 201
        assert actual_resp == expected_resp

        # test if s3.upload_image(path,image_name) is mocked and working
        image_name = f"{mock_uuid()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, image_name)
        s3_mock.assert_called_once_with(path, image_name)
