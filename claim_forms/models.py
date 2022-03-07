from django.db import models

# Create your models here.
class ClaimsForm(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='claim-forms', blank=True)


    def __str__(self):
        return self.title