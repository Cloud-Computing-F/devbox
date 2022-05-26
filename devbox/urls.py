from .Views import views, searchViews, deleteViews
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "devbox"

urlpatterns = [
    path("", views.home, name="home"),  # home directory
    path("<int:pk>/", views.change_directory, name="changeDirectory"),  # 디렉토리 이동

    path("uploadFile/<int:pk>/", views.uploadFile, name="uploadFile"),  # 파일 업로드
    path("downloadFile/<int:pk>/", views.downloadFile, name="downloadFile"),  # 파일 다운로드
    path("createFolder/<int:pk>/", views.createFolder, name="createFolder"),  # 폴더 생성
    path("deleteFileAndFolder/<int:pk>/", views.deleteFileAndFolder, name="deleteFileAndFolder"),  # 파일 및 폴더 삭제
    path("renameFileAndFolder/<int:pk>/", views.renameFileAndFolder, name="renameFileAndFolder"),  # 파일 및 폴더 이름 수정
    path("sortFileAndFolder/<int:pk>/", views.sortFileAndFolder, name="sortFileAndFolder"),  # 파일 정렬
    
    path("search/", searchViews.searchFileAndFolder, name="searchFileAndFolder"),  # 파일 검색
    path("sortFromSearch/<str:query>/", searchViews.sortFromSearch, name="sortFromSearch"),  # 파일 검색 후 정렬
    path("downloadFromSearch/<str:query>/", searchViews.downloadFromSearch, name="downloadFromSearch"),  # 파일 검색 후 다운로드
    path("deleteFromSearch/<str:query>/", searchViews.deleteFromSearch, name="deleteFromSearch"),  # 파일 검색 후 삭제

    path("recyclebin/", deleteViews.recyclebin, name="recyclebinDisplay"),  # 휴지통
    path("recyclebin/<int:pk>", deleteViews.changeDirectoryInRecyclebin, name="changeDirectoryInRecyclebin"),  # 휴지통 내 폴더 이동
    path("restore/<int:pk>", deleteViews.restore, name="restore"),  # 파일 및 폴더 복구
    path("permanentDelete/<int:pk>", deleteViews.permanentDelete, name="permanentDelete"),  # 파일 및 폴더 영구
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
