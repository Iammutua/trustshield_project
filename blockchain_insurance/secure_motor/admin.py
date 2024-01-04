from django.contrib import admin
from .models import Client

# Register your models here.

class CLientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "password", "date_joined")

admin.site.register(Client, CLientAdmin)
