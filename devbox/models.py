import os.path
from django.db import models
from django.utils.timezone import now


class Files(models.Model):
    fileName = models.CharField(max_length=100, default=now().strftime("%Y%m%d%H%M%S"))
    uploadedFile = models.FileField(upload_to="UploadedFiles/")
    dateTimeOfUpload = models.DateTimeField(auto_now=True)

    def get_filename(self):
        return os.path.basename(self.uploadedFile.name)
