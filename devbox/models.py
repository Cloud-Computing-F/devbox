import os.path
from django.db import models
from django.utils.timezone import now


class Folder(models.Model):
    folderName = models.CharField(max_length=100, default=now().strftime("%Y%m%d%H%M%S"))
    dateTimeOfUpload = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="child_folder", null=True, blank=True)

    def get_foldername(self):
        return self.folderName


class Files(models.Model):
    fileName = models.CharField(max_length=100, default=now().strftime("%Y%m%d%H%M%S"))
    fileSize = models.IntegerField(default=0)
    uploadedFile = models.FileField(upload_to="UploadedFiles/")
    dateTimeOfUpload = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="child_files", null=True, blank=True)

    def get_filename(self):
        return os.path.basename(self.uploadedFile.url)

    def delete(self, *args, **kwargs):
        super(Files, self).delete(*args, **kwargs)
        self.uploadedFile.delete()


class RecycleBins(models.Model):
    deletedFolderID = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="deleted_folder", null=True, blank=True)
    deletedFileID = models.ForeignKey(Files, on_delete=models.CASCADE, related_name="deleted_files", null=True, blank=True)
    dateTimeOfDelete = models.DateTimeField(auto_now=True)
