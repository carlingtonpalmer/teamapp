from django.db import models
from django.conf import settings
# Create your models here.


class Claim(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    claim_type = models.CharField(max_length=100)
    statement = models.TextField()
    doc = models.FileField(upload_to='files', max_length=1000, blank=False, null=False)

    def __str__(self):
        title_info = "{} ({})".format(self.claim_type, self.user)
        return title_info

    @property
    def filename(self):
        name = self.doc.name.split("/")[1].replace('_',' ').replace('-', ' ')
        return name
