import uuid
from django.db import models


class AbstractAPIKey(models.Model):

    class Meta:
        verbose_name_plural = "API Keys"
        ordering = ['-created']
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50, unique=True)
    key = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name
        
        
class APIKey(AbstractAPIKey):
    """
    Class for ApiKey authentication & permissions.
    Or define your own as: settings.DRF3_APIKEY_MODEL
    """
    class Meta(AbstractAPIKey.Meta):
        swappable = 'DRF3_APIKEY_MODEL'
