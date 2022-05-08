# Generated by Django 4.0.4 on 2022-05-06 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devbox', '0003_delete_blog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploadedFile', models.FileField(upload_to='UploadedFiles/')),
                ('dateTimeOfUpload', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Document',
        ),
    ]
