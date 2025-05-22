from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, UserData, GLS_Data

admin.site.register(User)
admin.site.register(UserData)
admin.site.register(GLS_Data)
