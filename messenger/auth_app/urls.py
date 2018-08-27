from django.urls import path
from . import views

# Путь от корня: account/
urlpatterns = [
    path('login', views.LogInView.as_view()),
    path('signin', views. SignInView.as_view()),
    path('logout', views.LogOutView.as_view()),
]