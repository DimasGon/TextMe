from django.urls import path
from . import views

# Путь от корня: account/
urlpatterns = [
    path('<int:pk>', views.AccountView.as_view()),
    path('<int:pk>/edit_profile', views.AccountSettingsView.as_view()),
    path('', views.AccountRedirectView.as_view())
]