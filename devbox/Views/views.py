import os
import zipfile
from io import BytesIO
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from devbox.models import Files, Folder, RecycleBins
from .utilsViews import sort, download


# Get parent folder name
def get_parent_folder_name(pk):
    parent_folders = []
    current_folder = Folder.objects.filter(id=pk if pk != 0 else None)
    while len(current_folder) > 0:
        parent_folders.insert(0, {"id": current_folder[0].id, "folderName": current_folder[0].folderName})
        if current_folder[0].parent_id is not None:
            current_folder = Folder.objects.filter(id=current_folder[0].parent_id)
        else:
            current_folder = []
    return parent_folders


# display file / folder
def display_file_and_folder(request, pk):
    files = list(Files.objects.filter(parent_id=pk if pk != 0 else None).order_by("fileName"))
    folders = list(Folder.objects.filter(parent_id=pk if pk != 0 else None).order_by("folderName"))

    not_deleted_files = []
    for file in files:
        if len(file.deleted_files.all()) == 0:
            not_deleted_files.append(file)
    print(not_deleted_files)

    not_deleted_folders = []
    for folder in folders:
        if len(folder.deleted_folder.all()) == 0:
            not_deleted_folders.append(folder)

    return render(request, "devbox/main.html", context={
        "current_folder_id": pk,
        "files": not_deleted_files,
        "folders": not_deleted_folders,
        "parentFolders": get_parent_folder_name(pk),
    })

# home directory
def home(request):
    return display_file_and_folder(request, 0)


# change directory
def change_directory(request, pk):
    return display_file_and_folder(request, pk)


# 파일 업로드
def uploadFile(request, pk):
    if request.method == "POST":
        selected = request.FILES.getlist("uploadFile")

        if len(selected) >= 1:
            for uploadedFile in request.FILES.getlist("uploadFile"):
                duplicated_file = Files.objects.filter(fileName=uploadedFile.name, parent_id=pk if pk != 0 else None)

                # 파일 업로드
                if len(duplicated_file) == 0:
                    file = Files(
                        uploadedFile=uploadedFile,
                        fileName=uploadedFile.name,
                        fileSize=uploadedFile.size,
                        parent_id=pk if pk != 0 else None,
                    )
                    file.save()

                # 같은 폴더에 이름 중복된 파일 예외 처리
                elif len(duplicated_file) >= 1:
                    print("중복된 파일 존재")

        # 업로드 할 파일이 선택되지 않는 경우 예외 처리
        elif len(selected) < 1:
            print("업로드할 파일을 선택해 주세요")

    # 파일 및 폴더 display
    return redirect("devbox:changeDirectory", pk)


# 파일 다운로드
@csrf_exempt
def downloadFile(request, pk):
    if request.method == "POST":
        selected = request.POST.getlist("selected_file")

        # 파일 다운로드
        if len(selected) >= 1:
            return download(selected)

        # 파일 선택 안함 예외 처리
        elif len(selected) < 1:
            print("다운로드할 파일을 선택해 주세요")
            return redirect("devbox:searchFileAndFolder")


# 폴더 생성
def createFolder(request, pk):
    if request.method == "POST":
        folderName = request.POST.get("createFolderName")

        if len(folderName) > 0:
            duplicated_folder = Folder.objects.filter(folderName=folderName, parent_id=pk if pk != 0 else None)

            # 폴더 생성
            if len(duplicated_folder) == 0:
                folder = Folder(
                    folderName=folderName,
                    parent_id=pk if pk != 0 else None,
                )
                folder.save()

            # 같은 폴더에 이름 중복된 폴더 예외 처리
            elif len(duplicated_folder) >= 1:
                print("중복된 폴더 존재")

                # 이름 입력 안함 예외 처리
        elif len(folderName) == 0:
            print("이름을 입력해 주세요")

    return redirect("devbox:changeDirectory", pk)


# 파일 및 폴더 삭제
@csrf_exempt
def deleteFileAndFolder(request, pk):
    if request.method == "POST":
        selected_folder = request.POST.getlist("selected_folder")
        selected_file = request.POST.getlist("selected_file")

        # 파일 및 폴더 선택 안함 예외 처리
        if len(selected_file) == 0 and len(selected_folder) == 0:
            print("삭제할 파일을 선택해 주세요")

        # 삭제
        else:
            # 선택한 폴더 삭제
            if len(selected_folder) >= 1:
                for folder_id in selected_folder:
                    deletedFolder = RecycleBins(
                        deletedFolderID_id=folder_id,
                    )
                    deletedFolder.save()

            # 선택한 파일 삭제
            if len(selected_file) >= 1:
                for file_id in selected_file:
                    deletedFile = RecycleBins(
                        deletedFileID_id=file_id,
                    )
                    deletedFile.save()

    return redirect("devbox:changeDirectory", pk)


# 파일 및 폴더 이름 수정
@csrf_exempt
def renameFileAndFolder(request, pk):
    if request.method == "POST":
        selected_folder = request.POST.getlist("selected_folder")
        selected_file = request.POST.getlist("selected_file")
        rename = request.POST.get("renameFileAndFolderName")

        # 파일 및 폴더 선택 안함 예외 처리
        if len(selected_file) == 0 and len(selected_folder) == 0:
            print("이름을 변경할 파일을 선택해 주세요")

        # 이름 입력 안함 예외 처리
        elif len(rename) == 0:
            print("수정할 이름을 입력해 주세요")

        # 이름 수정
        else:
            # 선택한 폴더 이름 수정
            if len(selected_folder) >= 1:
                for folder_id in selected_folder:
                    folder = Folder.objects.get(id=folder_id)
                    folder.folderName = rename
                    folder.save()

            # 선택한 파일 이름 수정
            if len(selected_file) >= 1:
                rename = rename.split('.')
                for file_id in selected_file:
                    file = Files.objects.get(id=file_id)
                    newFileName = rename[0]
                    extension = file.fileName.split('.')[-1] if len(rename) == 1 else rename[-1]
                    file.fileName = f"{newFileName}.{extension}"
                    file.save()

    return redirect("devbox:changeDirectory", pk)


# 파일 정렬
def sortFileAndFolder(request, pk):
    template = 'devbox/main.html'
    if request.method == "GET":
        sortMode = request.GET.get('sortFileAndFolder')
        files = Files.objects.filter(parent_id=pk if pk != 0 else None)
        folders = Folder.objects.filter(parent_id=pk if pk != 0 else None)

        context = sort(sortMode, files, folders)
        context["current_folder_id"] = pk
        context["parentFolders"] = get_parent_folder_name(pk)
        return render(request, template, context=context)
    else:
        return render(request, template)
