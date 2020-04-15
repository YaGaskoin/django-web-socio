from django.urls import path
from . import views
import django.contrib.auth.views as auth_views

app_name = "main"

urlpatterns = [
    path('', views.dashboard, name="main"),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(), name="login"),

]