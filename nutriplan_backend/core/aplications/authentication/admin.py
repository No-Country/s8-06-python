from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import Group
from .models import *

# Register your models here.
class UserAdmin(ModelAdmin):
    list_display = ('username',)


admin.site.register(User,UserAdmin)

admin.site.unregister(Group)



































