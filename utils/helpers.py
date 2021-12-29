import base64

from werkzeug.exceptions import BadRequest


def decode_image(path, encoded_string):
    try:
        with open(path, "wb") as file:
            file.write(base64.b64decode(encoded_string.encode("utf-8")))
    except Exception as ex:
        raise BadRequest("Invalid photo encoding")
