from django.urls import path
from . import views


app_name = "images"


urlpatterns = [
    #path('', ,name="images"),
    path('add/', views.add_image, name="add"),
]