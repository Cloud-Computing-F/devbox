# Generated by Django 4.0.4 on 2022-06-04 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devbox', '0007_files_username_folder_username_alter_files_filename_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='fileName',
            field=models.CharField(default='20220604194117', max_length=100),
        ),
        migrations.AlterField(
            model_name='folder',
            name='folderName',
            field=models.CharField(default='20220604194117', max_length=100),
        ),
    ]