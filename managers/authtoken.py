from datetime import datetime, timedelta

from decouple import config  # install python-decouple

# Basic and Digest HTTP authentication for Flask routes
from flask_httpauth import HTTPTokenAuth
from jwt import encode, decode, ExpiredSignatureError  # install pyJWT
from werkzeug.exceptions import Unauthorized, BadRequest

# Keep this imports because of the eval function
from models.users import Customer, Admin


# for SignUp,SignIn -> token = AuthTokenManager.encode_token(user)
# for Orders ->  @auth.login_required
class AuthTokenManager:
    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user.id,
            "exp": datetime.utcnow()
            + timedelta(
                days=100
            ),  # timedelta different for dev and production - JWT_DAYS
            "user_model": user.__class__.__name__,  # model name
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


# ---------- Authentication --------------------

# Bearer authentication (also called token authentication) is
# an HTTP authentication scheme that involves security tokens called bearer tokens.


auth = HTTPTokenAuth(scheme="Bearer")


# The client must send this token in the Authorization header
# when making requests to protected resources:
# https://learning.postman.com/docs/sending-requests/authorization/#bearer-token


# redefine HTTPTokenAuth method verify_token
# extend the token authentication against our custom implementation
@auth.verify_token
def verify_token(token):
    try:
        user_id, model_ = AuthTokenManager.decode_token(token)
        return eval(f"{model_}.query.filter_by(id={user_id}).first()")
        #  returns founded user in dB (with the extracted user.id)

    except Exception as ex:
        """
        invalid_token The access token provided is expired,
         revoked, malformed, or invalid for other reasons. 
        """
        raise Unauthorized("Invalid or missing token. Please log in again.")
