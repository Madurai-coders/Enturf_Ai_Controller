from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r'AIController/$', consumer.AIStatusConsumer.as_asgi()),
]