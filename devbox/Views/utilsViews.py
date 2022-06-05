from devbox.models import Files, Folder
from contents.models import Bucket
from django.db.models import Q
from io import BytesIO
from datetime import datetime
import os
import zipfile
from django.http import FileResponse, HttpResponse
from django.conf import settings
import boto3
import boto
import boto.s3.connection
import webbrowser


s3 = boto3.client('s3',
                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)


def get_bucket(request):
    bucketName = Bucket.objects.get(userName=request.user).bucketName
    return bucketName


# 다운로드 알고리즘
def download(request, selected):
    bucketName = get_bucket(request)
    conn = boto.s3.connect_to_region(settings.AWS_REGION,
                                     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                     is_secure=True,
                                     calling_format=boto.s3.connection.OrdinaryCallingFormat(),
                                     )
    bucket = conn.get_bucket(bucketName)
    for i in range(len(selected)):
        file = Files.objects.get(id=selected[i])

        aws_obj_key = bucket.get_key(str(file.uuid))
        headers = {
            'response-content-type': 'application/force-download',
            'response-content-disposition': f'attachment;filename={file.fileName}'
        }

        url = aws_obj_key.generate_url(
            response_headers=headers,
            expires_in=600,
        )
        webbrowser.open(url)
    return HttpResponse(url, status=200)


# 검색 알고리즘
def search(query):
    search_folder = Q(folderName__icontains=query)
    search_file = Q(fileName__icontains=query)
    obj_folders = Folder.objects.filter(search_folder).distinct().order_by('folderName')
    obj_files = Files.objects.filter(search_file).distinct().order_by('fileName')
    resSum = len(obj_files) + len(obj_folders)
    context = {
        'query': query,
        'obj_files': obj_files,
        'obj_folders': obj_folders,
        'resSum': resSum,
        'current_folder_id': 0,
    }
    return context


# 정렬 알고리즘-> 정렬 한 번 후 잘 안돌아감, 수정 필요
def sort(sortmode, files, folders):
    print(sortmode)
    if sortmode == 'title':  # 이름 순 정렬
        files = files.order_by('fileName')
        folders = folders.order_by('folderName')
    elif sortmode == 'size':  # 크기 순 정렬
        files = files.order_by('-fileSize')
        folders = folders.order_by('-folderName')  # 파일 크기가 없는 폴더는 이름 순으로 고정
    elif sortmode == "recent":  # 최신 순 정렬
        files = files.order_by('-dateTimeOfUpload')
        folders = folders.order_by('-dateTimeOfUpload')

    not_deleted_files = []
    for file in files:
        if len(file.deleted_files.all()) == 0:
            not_deleted_files.append(file)

    not_deleted_folders = []
    for folder in folders:
        if len(folder.deleted_folder.all()) == 0:
            not_deleted_folders.append(folder)

    context = {
        'files': not_deleted_files,
        'folders': not_deleted_folders,
    }
    return context
