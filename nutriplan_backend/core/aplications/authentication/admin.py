from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import Group
from .models import *

# Register your models here.
class UserAdmin(ModelAdmin):
    list_display = ('id','username',)


admin.site.register(User,UserAdmin)
admin.site.register(Profesional)

admin.site.unregister(Group)



































