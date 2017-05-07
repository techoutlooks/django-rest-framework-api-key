import binascii
import os

from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()
    
    
def get_apikey_model():
    try:
        conf_model = getattr(settings, 'DRF3_APIKEY_MODEL', 'rest_framework_api_key.APIKey')
        return django_apps.get_model(conf_model)
    except ValueError:
        raise ImproperlyConfigured("DRF3_APIKEY_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured("DRF3_APIKEY_MODEL refers to model '%s' that has not been installed" % conf_model)
