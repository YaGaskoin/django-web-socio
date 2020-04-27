from django.urls import path
from . import views


app_name = "images"


urlpatterns = [
    path('<int:page>/', views.images, name="images"),
    path('add/', views.add_image, name="add"),
    path('detail/<int:id>/<slug:slug>/', views.detail, name="detail"),
    path('image_like/', views.image_like, name='image_like'),
    path('ranking/', views.image_ranking, name='ranking'),
]