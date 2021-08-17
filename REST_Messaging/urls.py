
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    path('', include('api.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
