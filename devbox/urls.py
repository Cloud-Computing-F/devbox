from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

app_name = "devbox"

urlpatterns = [
    path("", login_required(views.home), name="home"),  # home directory
    path("<int:pk>/", views.change_directory, name="changeDirectory"),  # 디렉토리 이동

    path("uploadFile/<int:pk>/", views.uploadFile, name="uploadFile"),  # 파일 업로드
    path("downloadFile/<int:pk>/", views.downloadFile, name="downloadFile"),  # 파일 다운로드
    path("createFolder/<int:pk>/", views.createFolder, name="createFolder"),  # 폴더 생성
    path("deleteFileAndFolder/<int:pk>/", views.deleteFileAndFolder, name="deleteFileAndFolder"),  # 파일 및 폴더 삭제
    path("renameFileAndFolder/<int:pk>/", views.renameFileAndFolder, name="renameFileAndFolder"),  # 파일 및 폴더 이름 수정
    path("search/",login_required(views.search),name="search"),
    path("sh/<uuid:uuid>/",views.display_file_and_folder_ui,name='shared'),
    path("sortFile/<int:pk>/", views.sortFile, name="sortFile"),  # 파일 정렬
    path("mailing/",views.mailing, name="mailing"), # 메일링 
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
