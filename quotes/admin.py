from django.contrib import admin
from . import models

# Register your models here.

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('userId','quote_type', 'chassis','cost', 'vehicle_use', 'claim_free_driving')


admin.site.register(models.Quote, QuoteAdmin)