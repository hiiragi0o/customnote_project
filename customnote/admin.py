from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomUser


# 管理サイトにCustomUserモデルを登録
admin.site.register(CustomUser)  # Userモデルを登録
admin.site.unregister(Group)  # Groupモデルは不要のため非表示にします
