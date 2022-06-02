import os
import zipfile
from io import BytesIO
from datetime import datetime
from . import models
from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# display file / folder

def display_file_and_folder(request, pk):
    files = models.Files.objects.filter(parent_id=pk if pk != 0 else None)
    folders = models.Folder.objects.filter(parent_id=pk if pk != 0 else None)
    return render(request, "home.html", context={
        "current_folder_id": pk,
        "files": files,
        "folders": folders,
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
                duplicated_file = models.Files.objects.filter(fileName=uploadedFile.name, parent_id=pk if pk != 0 else None)
                
                # 파일 업로드
                if len(duplicated_file) == 0:
                    file = models.Files(
                        uploadedFile=uploadedFile,
                        fileName=uploadedFile.name,
                        fileSize=uploadedFile.size,
                        parent_id=pk if pk != 0 else None,
                    )

                    file.save()

                # 같은 폴더에 이름 중복된 파일 예외 처리
                elif len(duplicated_file) >= 1:
                    print("중복된 폴더 존재")

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

        # 파일 다중 선택 zip file로 다운로드
        if len(selected) > 1:
            zip_name = datetime.now()
            zip_name = zip_name.strftime("%Y%m%d%H%M%S")

            byte_data = BytesIO()
            with zipfile.ZipFile(byte_data, 'w', compression=zipfile.ZIP_DEFLATED) as myzip:
                for file_id in selected:
                    file = models.Files.objects.get(id=file_id)
                    file_path = os.path.basename(f"media/{file.uploadedFile}")
                    myzip.write(f"media/UploadedFiles/{file_path}", file.fileName)

            response = HttpResponse(byte_data.getvalue(), content_type="application/force-download")
            response['Content-Disposition'] = f'attachment; filename={zip_name}.zip'
            response['Content-Length'] = byte_data.tell()
            return response

        # 파일 단일 선택 원본 파일 다운로드
        elif len(selected) == 1:
            file = models.Files.objects.get(id=selected[0])
            file_path = os.path.basename(f"media/{file.uploadedFile}")
            file_system = FileSystemStorage(os.path.abspath("media/UploadedFiles/"))

            response = FileResponse(file_system.open(file_path), content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename="{file.fileName}"'
            return response
        
        # 파일 선택 안함 예외 처리
        elif len(selected) < 1:
            print("다운로드할 파일을 선택해 주세요")
            return redirect("devbox:changeDirectory", pk)


# 폴더 생성
def createFolder(request, pk):
    if request.method == "POST":
        folderName = request.POST.get("createFolderName")
        
        if len(folderName) > 0:
            duplicated_folder = models.Folder.objects.filter(folderName=folderName, parent_id=pk if pk != 0 else None)
    
            # 폴더 생성
            if len(duplicated_folder) == 0:
                folder = models.Folder(
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
                    folder = models.Folder.objects.get(id=folder_id)
                    folder.delete()

            # 선택한 파일 삭제
            if len(selected_file) >= 1:
                for file_id in selected_file:
                    file = models.Files.objects.get(id=file_id)
                    file.delete()

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
                    folder = models.Folder.objects.get(id=folder_id)
                    folder.folderName = rename
                    folder.save()

            # 선택한 파일 이름 수정
            if len(selected_file) >= 1:
                rename = rename.split('.')
                for file_id in selected_file:
                    file = models.Files.objects.get(id=file_id)
                    newFileName = rename[0]
                    extension = file.fileName.split('.')[-1] if len(rename) == 1 else rename[-1]
                    file.fileName = f"{newFileName}.{extension}"
                    file.save()

    return redirect("devbox:changeDirectory", pk)


def search(request):
    template = 'devbox/search_result.html'
    if request.method == "GET":
        query = request.GET.get('search_input')
        if query is not None:
            search_folder = Q(folderName__icontains=query)
            search_file = Q(fileName__icontains=query)
            obj_folder = models.Folder.objects.filter(search_folder).distinct()
            obj_file = models.Files.objects.filter(search_file).distinct()
            resSum = len(obj_file)+len(obj_folder)
            context = {'obj_file':obj_file,'obj_folder':obj_folder,'resSum':resSum}
            return render(request,template,context)
        else : 
            return render(request,template)
    else :
        return render(request,template)
            
def share_folder(request):
    template = 'devbox/share_folder_link.html'
    if request.method=='POST' :
        selected_folder = request.POST.getlist("selected_folder")
        if len(selected_folder)==0 :
            print("공유하고 싶은 폴더를 선택해주세요")
            
        else : 
            for folder_id in selected_folder:
                folder = models.Folder.objects.get(id=folder_id)
                return render(request,template,context={
                    'address':'127.0.0.1:8000/sh/'+str(folder.uuid),
                    'uuid':folder.uuid
                })
                
def sortFile(request, pk):
    sort = request.GET.get('sort', 'recent')
    # 파일명순
    if sort == 'title':
        files = Files.objects.order_by(
            '-fileName', '-dateTimeOfUpload')
    # 크기순
    elif sort == 'size':
        files = Files.objects.order_by('-fileSize', '-dateTimeOfUpload')
    # 파일 생성일순
    else:
        files = Files.objects.order_by(
            '-dateTimeOfUpload', '-dateTimeOfUpload')
    folders = models.Folder.objects.filter(parent_id=pk if pk != 0 else None)
    return render(request, 'devbox/main.html', {'files': files, 'folders': folders, 'sort': sort, 'current_folder_id': pk})

# folder 공유 서비스 
def display_file_and_folder_ui(request,uuid):
    folders = models.Folder.objects.filter(uuid=uuid)
    files = models.Files.objects.filter(parent_id=0)
    return render(request,"home.html",context={
        "current_folder_id": 0 ,
        "files": files,
        "folders": folders,
    })

# 메일링 서비스 
@csrf_exempt
def mailing(request):
    if request.method=='POST' :
        # 파일 혹은 폴더 선택
        selected_target = request.POST.get('selected_target')
        # 이메일 주소 입력 -> (2022.05.22 기준 이메일 하나만 작성가능)
        email_address = request.POST.get('email_address')
        recipient_list = [email_address]
        # 'devbox/mail.html' 에서 mailing 시 들어갈 email 화면을 꾸밀 수 있습니다. 
        html_message=render_to_string('devbox/mail.html',context={
            # 주소는 공유 파일/폴더 주소에 맞게 수정하면 됩니다.
            # 우선은 가장 기본적인 것으로 설정해뒀습니다.
            'link':selected_target,
        })
        # send_mail (메일 제목, 메일 내용, email_from,recipient_list,html_message)
        send_mail("DevBox 공유 메일","테스트 내용입니다.",settings.EMAIL_HOST_USER,recipient_list,html_message=html_message)
        # 바로 홈 화면으로 넘어갑니다. 
        return display_file_and_folder(request, 0)

