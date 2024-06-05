from django.contrib import admin
from .models import YourModel


class YourModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(YourModel, YourModelAdmin)
