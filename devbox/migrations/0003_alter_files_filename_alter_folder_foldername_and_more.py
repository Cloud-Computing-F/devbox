# Generated by Django 4.0.4 on 2022-05-25 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devbox', '0002_alter_files_filename_alter_folder_foldername'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='fileName',
            field=models.CharField(default='20220525162702', max_length=100),
        ),
        migrations.AlterField(
            model_name='folder',
            name='folderName',
            field=models.CharField(default='20220525162702', max_length=100),
        ),
        migrations.CreateModel(
            name='RecycleBins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTimeOfDelete', models.DateTimeField(auto_now=True)),
                ('deletedFileID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delete_files', to='devbox.files')),
                ('deletedFolderID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deleted_folder', to='devbox.folder')),
            ],
        ),
    ]
