from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .serializers import UserSerializer,AIStatusSerializer
from .models import AIStatus

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AIStatusViewset(viewsets.ModelViewSet):
    queryset = AIStatus.objects.all()
    serializer_class = AIStatusSerializer