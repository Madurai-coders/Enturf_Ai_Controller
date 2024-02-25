from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .serializers import UserSerializer,AIStatusSerializer,GallerySerializer
from .models import AIStatus,Gallery
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AIStatusViewset(viewsets.ModelViewSet):
    queryset = AIStatus.objects.all()
    serializer_class = AIStatusSerializer

class GalleryViewset(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    
    def retrieve(self, request, *args, **kwargs):
        video_path = kwargs.get('video_path')
        print(video_path)
        queryset = self.queryset.filter(videoPath=video_path)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
from django.http import HttpResponse
from django.http import FileResponse, HttpResponseNotFound
import os
import mimetypes

def serve_m3u8(request, playlist_name):
    # Base directory where your .m3u8 files are located
    playlists_dir = 'C:/Users/Kaamil/Documents/Enturf_Ai_Controller/media/rec'

    # Construct the full path to the .m3u8 file
    playlist_path = os.path.normpath(os.path.join(playlists_dir, playlist_name))
    # Security check: Ensure the constructed path is within playlists_dir
    if not playlist_path.startswith(os.path.abspath(playlists_dir)):
        return HttpResponseNotFound('Playlist not found')

    # Check if the .m3u8 file exists and is a file
    if not os.path.isfile(playlist_path):
        return HttpResponseNotFound('Playlist not found')

    content_type, _ = mimetypes.guess_type(playlist_path)
    if content_type is None:
        # Default MIME type if the type cannot be guessed
        content_type = 'application/octet-stream'

    # Serve the file
    try:
        return FileResponse(open(playlist_path, 'rb'), content_type=content_type)
    except IOError:
        # Handle error if file could not be opened
        return HttpResponseNotFound('Error opening file')
