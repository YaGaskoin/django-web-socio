from django.urls import path
from . import views
import django.contrib.auth.views as auth_views


urlpatterns = [
    path('', views.dashboard, name="main"),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('change_password/', auth_views.PasswordChangeView.as_view(), name="change_password"),
    path('change_password/done', auth_views.PasswordChangeDoneView.as_view(), name="change_password_done"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view() , name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('edit/', views.edit, name="edit"),

]