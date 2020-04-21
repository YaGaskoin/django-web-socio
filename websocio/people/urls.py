from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'people'


urlpatterns = [
    path('<int:page>/', views.people, name='people'),
    path('user_detail/<int:id>/', views.user_detail, name='user_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
