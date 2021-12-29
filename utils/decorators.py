from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from managers.authtoken import auth


def validate_schema(schema_name):
    def wrapper(func):
        def decorated_func(*args, **kwargs):
            data = request.get_json()
            schema = schema_name()
            errors = schema.validate(data)
            if errors:
                raise BadRequest(f"Invalid data fields - {', '.join(errors)}")
            return func(*args, **kwargs)

        return decorated_func

    return wrapper


# Authorization decorator - permissions is a [list of customer,staff,admin]
def permission_required(permissions):
    def wrapper(func):
        def decorated_func(*args, **kwargs):
            # authenticated user
            user = (
                auth.current_user()
            )  # current user is returned from verify_token founded in db
            if user.role not in permissions:
                raise Forbidden("You don't have access to this resource")  # 403
            return func(*args, **kwargs)

        return decorated_func

    return wrapper
