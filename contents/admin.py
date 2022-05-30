from django.contrib import admin

# Register your models here.
from contents.models import Content,  FollowRelation


class FollowRelationAdmin(admin.ModelAdmin):
    pass

admin.site.register(FollowRelation, FollowRelationAdmin)