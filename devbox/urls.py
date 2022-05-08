from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "devbox"

urlpatterns = [
    path("upload/", views.uploadFile, name="uploadFile"),
    path("download/", views.downloadFile, name="downloadFile"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
