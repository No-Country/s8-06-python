from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import Group
from .models import *

# Register your models here

admin.site.register(Post_recipe)
