from datetime import datetime, timedelta

from decouple import config
from flask_httpauth import HTTPTokenAuth
from jwt import encode, decode
from werkzeug.exceptions import Unauthorized


""" Keep this imports because of the eval function
    from models.users import Customer, Admin, Staff
"""
from models.users import Customer, Admin, Staff

class AuthTokenManager:
    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user.id,
            "exp": datetime.utcnow() + timedelta(days=100),
            "user_model": user.__class__.__name__,
        }
        return encode(payload, key=config("JWT_SECRET_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            payload = decode(
                jwt=token, key=config("JWT_SECRET_KEY"), algorithms=["HS256"]
            )
            return payload["sub"], payload["user_model"]
        except Exception as ex:
            raise ex


# Bearer authentication object token
auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    """
     redefine HTTPTokenAuth method verify_token, so extend
     the token authentication against our custom implementation;
     if the token is valid:
         returns founded user in dB with the extracted user.id
     Raises error if the token is invalid - is expired,revoked, malformed,
         or invalid for other reasons.
    """
    try:
        user_id, model_ = AuthTokenManager.decode_token(token)
        return eval(f"{model_}.query.filter_by(id={user_id}).first()")
    except Exception as ex:
        raise Unauthorized("Invalid or missing token. Please log in again.")
