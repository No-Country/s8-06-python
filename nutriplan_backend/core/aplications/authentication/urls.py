from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('', buscar_recetas, name='buscar_recetas'),
]