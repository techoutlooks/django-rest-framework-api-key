from rest_framework import permissions
from .helpers import get_apikey_model


class HasAPIAccess(permissions.BasePermission):
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_API_KEY', '')
        return get_apikey_model().objects.filter(key=api_key).exists()
