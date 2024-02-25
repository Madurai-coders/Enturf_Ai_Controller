from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIStatusViewset,GalleryViewset,serve_m3u8

router = DefaultRouter()
router.register(r'AIStatus', AIStatusViewset, basename='crud_admin')
router.register(r'Gallery', GalleryViewset, basename='gallery_admin')
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include(router.urls)),
    path('gallery/<path:video_path>/', GalleryViewset.as_view({'get': 'retrieve'}), name='gallery-detail'),
    path('hls/<path:playlist_name>', serve_m3u8, name='serve_m3u8'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)