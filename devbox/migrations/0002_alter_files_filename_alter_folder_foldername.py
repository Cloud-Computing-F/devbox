# Generated by Django 4.0.4 on 2022-06-03 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devbox', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='fileName',
            field=models.CharField(default='20220603154030', max_length=100),
        ),
        migrations.AlterField(
            model_name='folder',
            name='folderName',
            field=models.CharField(default='20220603154030', max_length=100),
        ),
    ]
