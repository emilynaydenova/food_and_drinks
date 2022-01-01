from managers.authtoken import AuthTokenManager


def generate_token(user):
    return AuthTokenManager.encode_token(user)


def mock_uuid():
    return "11111111-1111-1111-1111-111111111111"
