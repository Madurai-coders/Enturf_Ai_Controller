from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import AIStatus,Gallery
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class AIStatusSerializer(serializers.ModelSerializer):
    #user = serializers.CharField(source='user.username',read_only=True)

    class Meta:
        model = AIStatus
        fields = ['user', 'previousState', 'currentState', 'mobileNumber',
                  'duration', 'status_change_time']


class GallerySerializer(serializers.ModelSerializer):
    #user = serializers.CharField(source='user.username',read_only=True)

    class Meta:
        model = Gallery
        fields = ['videoPath', 'my_array']