from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ユーザー登録のためのAPI
    path('api/customnote/', include('customnote.urls')),

    # アプリ
    path('customnote/', include('customnote.urls')),
]
