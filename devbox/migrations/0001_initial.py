# Generated by Django 4.0.4 on 2022-05-12 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folderName', models.CharField(default='20220512091351', max_length=100)),
                ('dateTimeOfUpload', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_folder', to='devbox.folder')),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(default='20220512091351', max_length=100)),
                ('fileSize', models.IntegerField(default=0)),
                ('uploadedFile', models.FileField(upload_to='UploadedFiles/')),
                ('dateTimeOfUpload', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_files', to='devbox.folder')),
            ],
        ),
    ]
