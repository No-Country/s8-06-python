from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('getroom/', ShowRoom.as_view(), name='getroom'),
    path('getrooms/', ShowRoomsUser.as_view(), name='getrooms'),
    path('newroom/', NewRoom.as_view(), name='newroom'),
    path('send/', SendMessage.as_view(), name='send'),
    path('getMessages/', ShowListMessages.as_view(), name='getMessages'),
]