from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


""" カスタムユーザーモデルを定義 """
class CustomUser(AbstractUser):
    # 追加フィールド（例）
    nickname = models.CharField(max_length=30, verbose_name='ニックネーム')
    email = models.EmailField(unique=True, verbose_name='メールアドレス') # メールアドレスを必須かつユニークに
    # 管理ユーザー
    is_manager = models.BooleanField(default=False, verbose_name='管理者権限') # 管理者権限を持つかどうか

    USERNAME_FIELD = 'email' # メールアドレスでログインさせる
    REQUIRED_FIELDS = ['username'] # USERNAME_FIELDがemailの場合、createsuperuserでusernameも入力させる

    def __str__(self):
        return self.email


""" カスタムメニューを定義 """
class CustomMenu(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='custom_menus')
    shop = models.CharField(max_length=100)  # 例: Starbucks
    category = models.CharField(max_length=50)  # 例: ドリンク, フード
    base_menu = models.CharField(max_length=100)  # 例: キャラメルマキアート
    temperature = models.CharField(max_length=20, blank=True)  # 例: Hot, Iced
    option = models.TextField(blank=True)  # 例: ホイップ追加、シロップ変更など
    tags = models.CharField(max_length=100, blank=True)  # 例: 季節限定, chill
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.base_menu} ({self.shop})"
