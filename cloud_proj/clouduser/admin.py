from django.contrib import admin
from .models import Clouduser
# Register your models here.
class ClouduserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')


admin.site.register(Clouduser, ClouduserAdmin)
