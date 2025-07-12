from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

import hashlib
from datetime import timedelta
from django.utils import timezone


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


""" アクセストークンを定義 """
# アクセストークンの有効期限を30日後に設定
def in_30_days():
    return timezone.now() + timedelta(days=30)


class AccessToken(models.Model):
    # ひもづくユーザー
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # アクセストークン(max_lengthが40に設定されている理由は、トークンはsha1でハッシュ化した文字列を設定するため)
    token = models.CharField(max_length=40)
    # アクセス日時
    access_datetime = models.DateTimeField(default=in_30_days)

    def __str__(self):
        # メールアドレスとアクセス日時、トークンが見えるように設定
        dt = timezone.localtime(self.access_datetime).strftime("%Y/%m/%d %H:%M:%S")
        return self.user.email + '(' + dt + ') - ' + self.token

    @staticmethod
    def create(user: CustomUser):
        # ユーザの既存のトークンを取得
        if AccessToken.objects.filter(user=user).exists():
            # トークンがすでに存在している場合は削除
            AccessToken.objects.get(user=user).delete()

        # トークン作成（email + システム日付のハッシュ値とする）
        #　パスワード情報をトークン生成に使わない。# あとでランダムなトークン生成に調整する
        dt = timezone.now()
        str = user.email + dt.strftime('%Y%m%d%H%M%S%f')
        hash = hashlib.sha1(str.encode('utf-8')).hexdigest()

        # トークンをDBに追加
        token = AccessToken.objects.create(
            user=user,
            token=hash,
            access_datetime=dt)

        return token


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
