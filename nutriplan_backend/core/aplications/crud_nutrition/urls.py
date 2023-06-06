from django.urls import path
from .views import *

urlpatterns = [
    path('recipes/', find_recipe, name='find_recipe'),
    path('create/', post_create, name='create_post'),
    path('list/<int:pk>/', post_detail, name='detail_post'),
    path('list/', post_list, name='list_post'),
    path('edit/<int:pk>/', post_edit, name='edit_post'),
    path('delete/<int:pk>/', post_delete, name='delete_post'),
    path('favorites', favorites_view, name='favorites_view'  ),
]

