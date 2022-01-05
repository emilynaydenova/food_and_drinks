from password_strength import PasswordPolicy
from werkzeug.exceptions import BadRequest
from werkzeug.routing import ValidationError

from models import CategoryEnum


def validate_category(category_value):
    values = [e.value for e in CategoryEnum]
    if category_value not in values:
        raise BadRequest("No such category name.")


policy = PasswordPolicy.from_names(
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 1 digits
    special=1,  # need min. 1 special characters
    nonletters=1,  # need min. 1 non-letter characters (digits, specials, anything)
)


def validate_password(value):
    errors = policy.test(value)
    if errors:
        raise ValidationError(f"Not a valid password")

