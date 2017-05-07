# -*- coding: utf-8 -*-
__author__ = 'ceduth'

from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from .helpers import get_apikey_model


APIKey = get_apikey_model()

class ApiKeyAuthentication(TokenAuthentication):
    """ 
    Does not use the "Authorization" HTTP header to get the token key,
    instead, use request headers of 'HTTP_API_KEY'; eg:

    curl http://localhost:8000/accounts/api/v1/ -H "Api-Key:xxxxx"
    http GET http://localhost:8000/accounts/api/v1/ Api-Key:xxxxx
    """

    def get_token_from_auth_header(self, auth):
        auth = auth.split()
        if not auth or auth[0].lower() != b'api-key':
            return None

        if len(auth) == 1:
            raise AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            return auth[1].decode()
        except UnicodeError:
            raise AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')

    def authenticate(self, request):
        auth = get_authorization_header(request)
        token = self.get_token_from_auth_header(auth)

        if not token:
            token = request.GET.get('api-key', request.POST.get('api-key', None))

        if token:
            return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            token = APIKey.objects.get(key=key)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid Api key.')

        if not token.is_active:
            raise AuthenticationFailed('Api key inactive or deleted.')
