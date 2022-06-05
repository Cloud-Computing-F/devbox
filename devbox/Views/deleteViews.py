from django.shortcuts import render, redirect
from devbox.models import Files, Folder, RecycleBins
from .utilsViews import sort
from django.conf import settings
from contents.models import Bucket
import boto3


s3 = boto3.client('s3',
                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)


def get_bucket(request):
    bucketName = Bucket.objects.get(userName=request.user).bucketName
    return bucketName


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
def changeDirectoryInRecyclebin(request, pk):
    files = list(Files.objects.filter(parent_id=pk if pk != 0 else None).order_by("fileName"))
    folders = list(Folder.objects.filter(parent_id=pk if pk != 0 else None).order_by("folderName"))

    return render(request, "recyclebin.html", context={
        "current_folder_id": pk,
        "files": files,
        "folders": folders,
        "parentFolders": get_parent_folder_name(pk),
    })


# display root recyclebin
def recyclebin(request):
    deletedfiles = RecycleBins.objects.filter(deletedFolderID_id=None)
    deletedfolders = RecycleBins.objects.filter(deletedFileID_id=None)

    files = []
    for deletedfile in deletedfiles:
        files.append(Files.objects.get(id=deletedfile.deletedFileID_id))

    folders = []
    for deletedfolder in deletedfolders:
        folders.append(Folder.objects.get(id=deletedfolder.deletedFolderID_id))

    return render(request, "recyclebin.html", context={
        "current_folder_id": 0,
        "files": files,
        "folders": folders,
    })


# 파일 복구
def restore(request, pk):
    if request.method == "POST":
        selected_folder = request.POST.getlist("selected_folder")
        selected_file = request.POST.getlist("selected_file")

        # 파일 및 폴더 선택 안함 예외 처리
        if len(selected_file) == 0 and len(selected_folder) == 0:
            print("복구할 파일을 선택해 주세요")

        # 복구
        else:
            # 선택한 폴더 복구
            if len(selected_folder) >= 1:
                for folder_id in selected_folder:
                    deletedFolder = RecycleBins.objects.filter(deletedFolderID_id=folder_id)
                    if len(deletedFolder) == 0:
                        print("상위 폴더가 존재하지 않습니다.")
                    deletedFolder.delete()

            # 선택한 파일 복구
            if len(selected_file) >= 1:
                for file_id in selected_file:
                    deletedFile = RecycleBins.objects.filter(deletedFileID_id=file_id)
                    if len(deletedFile) == 0:
                        print("상위 파일이 존재하지 않습니다.")
                    deletedFile.delete()

    if pk == 0:
        return redirect("devbox:recyclebinDisplay")
    elif pk != 0:
        return redirect("devbox:changeDirectoryInRecyclebin", pk)


# 파일 영구 삭제
def permanentDelete(request, pk):
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
                deleted_file_list = []
                deleted_folder_list = []
                for folder_id in selected_folder:
                    temp_deleted_folder_list = []
                    temp_deleted_folder_list.append(Folder.objects.get(id=folder_id))
                    deleted_folder_list.append(Folder.objects.get(id=folder_id))

                    # 하위 폴더 및 파일 담기
                    while len(temp_deleted_folder_list) != 0:
                        temp_deleted_folder_list += temp_deleted_folder_list[0].child_folder.all()
                        deleted_folder_list += temp_deleted_folder_list[0].child_folder.all()
                        deleted_file_list += temp_deleted_folder_list[0].child_files.all()
                        temp_deleted_folder_list.pop(0)

                # 파일 삭제
                for file_id in deleted_file_list:
                    file = Files.objects.filter(id=file_id.id)[0]
                    s3.delete_object(Bucket=get_bucket(request), Key=str(file.uuid))
                    file.delete()

                # 폴더 삭제
                for folder_id in deleted_folder_list:
                    folder = Folder.objects.filter(id=folder_id.id)
                    folder.delete()

            # 선택한 파일 삭제
            if len(selected_file) >= 1:
                for file_id in selected_file:
                    file = Files.objects.filter(id=file_id)[0]
                    s3.delete_object(Bucket=get_bucket(request), Key=str(file.uuid))
                    file.delete()

    if pk == 0:
        return redirect("devbox:recyclebinDisplay")
    elif pk != 0:
        return redirect("devbox:changeDirectoryInRecyclebin", pk)


# 파일 정렬 (수정)
# def sortFileAndFolder(request, pk):
#     template = 'devbox/main.html'
#     if request.method == "GET":
#         sortMode = request.GET.get('sortFileAndFolder')
#         files = Files.objects.filter(parent_id=pk if pk != 0 else None)
#         folders = Folder.objects.filter(parent_id=pk if pk != 0 else None)
#
#         context = sort(sortMode, files, folders)
#         context["current_folder_id"] = pk
#         context["parentFolders"] = get_parent_folder_name(pk)
#         return render(request, template, context=context)
#     else:
#         return render(request, template)
