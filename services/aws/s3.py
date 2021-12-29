import boto3
from botocore.exceptions import ClientError

from decouple import config
from werkzeug.exceptions import InternalServerError


class S3Service:
    def __init__(self):
        self.key = config("AWS_ACCESS_KEY")
        self.secret = config("AWS_SECRET")
        self.bucket_name = config("AWS_BUCKET")
        self.region = config("AWS_REGION")

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret,
        )

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_file
    def upload_image(self, file_name, object_name):
        """
        Upload a file to an S3 bucket
            :param file_name: File to upload
            :param bucket_name: Bucket to upload to
            :param object_name: S3 object name. If not specified then file_name is used
            :return: Object URL of image_file on s3

        """
        try:
            ext = file_name.split(".")[-1]
            self.s3.upload_file(file_name, self.bucket_name, object_name)
        except ClientError as e:
            raise InternalServerError("Provider is not available at the moment")

        image_s3_url = (
            f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{object_name}"
        )
        return image_s3_url

    # in boto3 can define policies programmatically -> ExtraArgs={'ACL': 'public-read',} -
    # private or public separate files

    def delete_image(self, object_url):
        """
        Delete a file from S3 bucket.
        """
        url_prefix = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/"
        object_name = object_url.replace(url_prefix, "")
        try:
            response = self.s3.delete_object(Bucket=self.bucket_name, Key=object_name)
        except ClientError as e:
            raise InternalServerError("Provider is not available at the moment")

        return response


# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
