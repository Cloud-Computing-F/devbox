import os
import zipfile
from io import BytesIO
from datetime import datetime
from . import models
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt


def uploadFile(request):
    if request.method == "POST":
        # Fetching the form data
        uploadedFile = request.FILES["uploadedFile"]

        # Saving the information in the database
        document = models.Files(
            uploadedFile=uploadedFile,
            fileName=uploadedFile.name,
        )
        document.save()

    documents = models.Files.objects.all()

    return render(request, "devbox/upload-file.html", context={
        "files": documents,
    })


@csrf_exempt
def downloadFile(request):
    if request.method == "POST":
        selected = request.POST.getlist("selected")

        if len(selected) > 1:
            zip_name = datetime.now()
            zip_name = zip_name.strftime("%Y%m%d%H%M%S")
            byte_data = BytesIO()
            with zipfile.ZipFile(byte_data, 'w', compression=zipfile.ZIP_DEFLATED) as myzip:
                for file in selected:
                    myzip.write(f"media/UploadedFiles/{file}", file)

            response = HttpResponse(byte_data.getvalue(), content_type="application/force-download")
            response['Content-Disposition'] = f'attachment; filename={zip_name}.zip'
            response['Content-Length'] = byte_data.tell()

        else:
            file_system = FileSystemStorage(os.path.abspath("media/UploadedFiles/"))
            file_name = os.path.basename(f"media/UploadedFiles/{selected[0]}")
            response = FileResponse(file_system.open(file_name),
                                    content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    return response

