from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from .models import Content

content_type = ContentType.objects.get_for_model(Content)
content_permission = Permission.objects.filter(content_type=content_type)

print([perm.codenmae for perm in content_permission])
