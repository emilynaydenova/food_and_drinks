import os
import uuid

from psycopg2 import DatabaseError
from werkzeug.exceptions import BadRequest

from constants import TEMP_FILE_FOLDER
from db import db
from models import Category, CategoryEnum
from services.aws.s3 import S3Service
from utils.helpers import decode_image

s3 = S3Service()


def s3_image_upload(data):

    # set a random image's file name - to upload in S3
    image_file_name = f'{str(uuid.uuid4())}.{data.pop("image_extension")}'
    path = os.path.join(TEMP_FILE_FOLDER, image_file_name)
    decode_image(path, data.pop("image"))
    try:
        data["image_url"] = s3.upload_image(path, image_file_name)
    except Exception as ex:
        raise BadRequest("Provider error uploading image")
    finally:
        os.remove(path)
    return data


def find_category(id_):
    category = Category.query.filter_by(id=id_).first()
    if not category:
        raise BadRequest(f"Category does not exist")
    return category


class CategoryManager:
    # Read
    @staticmethod
    def get_all_categories():
        return Category.query.all()

    # Create
    @staticmethod
    def create(category_data):
        value = category_data["title"]
        title = CategoryEnum(value).name

        if Category.query.filter_by(title=title).first():
            raise BadRequest(f"Category #{value}# already exists")

        category_data["title"] = title
        data = s3_image_upload(category_data)

        category = Category(**data)
        db.session.add(category)
        db.session.commit()

        category = Category.query.filter_by(title=title).first()
        return category

    # Update - can activate/deactivate a category
    @staticmethod
    def update(category_data, id_):
        # title is validated in @validate_schema
        del category_data["title"]  # because can't be changed via update

        category = find_category(id_)

        # replace image in S3 = delete the old one + upload a new one
        s3.delete_image(category.image_url)
        data = s3_image_upload(category_data)
        Category.query.filter_by(id=id_).update(data)
        db.session.commit()

        category = Category.query.filter_by(id=id_).first()
        return category

    @staticmethod
    def delete(id_):
        category = find_category(id_)

        # find all food and drinks to this category - ask to delete them first
        try:
            s3.delete_image(category.image_url)
            db.session.delete(category)
            db.session.commit()
        except Exception as e:
            raise BadRequest("Delete food and drinks items connected to this category first.")
        return category

    @staticmethod
    def get(id_):
        category = find_category(id_)
        return category
