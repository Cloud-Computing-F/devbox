from devbox.models import Files, Folder
from django.db.models import Q
from io import BytesIO
from datetime import datetime
import os
import zipfile
from django.http import FileResponse, HttpResponse
from django.core.files.storage import FileSystemStorage


# 다운로드 알고리즘
def download(selected):
    if len(selected) > 1:
        zip_name = datetime.now()
        zip_name = zip_name.strftime("%Y%m%d%H%M%S")

        byte_data = BytesIO()
        with zipfile.ZipFile(byte_data, 'w', compression=zipfile.ZIP_DEFLATED) as myzip:
            for file_id in selected:
                file = Files.objects.get(id=file_id)
                file_path = os.path.basename(f"media/{file.uploadedFile}")
                myzip.write(f"media/UploadedFiles/{file_path}", file.fileName)

        response = HttpResponse(byte_data.getvalue(), content_type="application/force-download")
        response['Content-Disposition'] = f'attachment; filename={zip_name}.zip'
        response['Content-Length'] = byte_data.tell()
        return response

    # 파일 단일 선택 원본 파일 다운로드
    elif len(selected) == 1:
        file = Files.objects.get(id=selected[0])
        file_path = os.path.basename(f"media/{file.uploadedFile}")
        file_system = FileSystemStorage(os.path.abspath("media/UploadedFiles/"))

        response = FileResponse(file_system.open(file_path), content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{file.fileName}"'
        return response


# 검색 알고리즘
def search(query):
    search_folder = Q(folderName__icontains=query)
    search_file = Q(fileName__icontains=query)
    obj_folders = Folder.objects.filter(search_folder).distinct().order_by("folderName")
    obj_files = Files.objects.filter(search_file).distinct().order_by("fileName")
    resSum = len(obj_files) + len(obj_folders)
    context = {
        'query': query,
        'files': obj_files,
        'folders': obj_folders,
        'resSum': resSum
    }
    return context


# 정렬 알고리즘
def sort(sortmode, files, folders):
    if sortmode == 'title':  # 이름 순 정렬
        files = files.order_by('fileName')
        folders = folders.order_by('folderName')
    elif sortmode == 'size':  # 크기 순 정렬
        files = files.order_by('-fileSize')
        folders = folders.order_by('-folderName')  # 파일 크기가 없는 폴더는 이름 순으로 고정
    elif sortmode == "recent":  # 최신 순 정렬
        files = files.order_by('-dateTimeOfUpload')
        folders = folders.order_by('-dateTimeOfUpload')

    context = {
        'files': files,
        'folders': folders,
    }
    return context

