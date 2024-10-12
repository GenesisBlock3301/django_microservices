import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .user import CustomUser


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Get the token from the request's Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Token '):
            return None

        token = auth_header.split(' ')[1]
        return self._validate_token(token, settings.CONFIG.JWT_SECRET_KEY)

    @staticmethod
    def _validate_token(token, jwt_secret_key):
        try:
            # Decode the token using the same secret key used to issue the token
            payload = jwt.decode(token, jwt_secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        # Retrieve the user information from the payload
        user_id = payload.get('user_id')
        user_type = payload.get('user_type')
        if not user_id or not user_type:
            raise exceptions.AuthenticationFailed('Invalid token: no user ID')

        user = CustomUser({"user_id": user_id, "user_type": user_type, "token": token})

        return user, None
