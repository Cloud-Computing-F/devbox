# Generated by Django 4.0.4 on 2022-06-04 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devbox', '0003_alter_files_filename_alter_folder_foldername'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='fileName',
            field=models.CharField(default='20220604090953', max_length=100),
        ),
        migrations.AlterField(
            model_name='folder',
            name='folderName',
            field=models.CharField(default='20220604090953', max_length=100),
        ),
    ]
