from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIStatusViewset

router = DefaultRouter()
router.register(r'AIStatus', AIStatusViewset, basename='crud_admin')


urlpatterns = [
    path('', include(router.urls)),
]
