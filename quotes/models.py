from django.db import models
from django.conf import settings

# Create your models here.


class Quote(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quote_type = models.CharField(max_length=50)
    chassis = models.CharField(max_length=100)
    cost = models.CharField(max_length=10)
    vehicle_use = models.CharField(max_length=50)
    claim_free_driving = models.CharField(max_length=200)

    def __str__(self):
        quote_title = "{} ({})".format(self.quote_type, self.userId)
        return quote_title