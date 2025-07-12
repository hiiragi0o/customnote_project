# シリアライザは、Django REST Frameworkを使用してモデルのデータをJSON形式に変換する
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomUser, CustomMenu


""" カスタムユーザーモデルのシリアライザ """
# ユーザー登録用のシリアライザ(名前このままでいい)
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'nickname', 'password')
        # パスワードは書き込み専用に設定
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        # usernameがなければemailから自動生成
        if 'username' not in validated_data:
            validated_data['username'] = validated_data['email']
        # 新しいユーザーを作成
        user = CustomUser.objects.create_user(**validated_data)

        return user

# サインイン用のシリアライザ
class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('メールアドレスまたはパスワードが正しくありません。')
        
        data['user'] = user

        return data

# ユーザー情報更新用のシリアライザ
class UserUpdateSerializer(serializers.ModelSerializer):
    """
    ユーザー情報（ニックネームなど）を更新するためのSerializer
    メールアドレスやユーザー名は通常、このAPIでは更新しません。
    """
    class Meta:
        model = CustomUser
        fields = ('nickname',) # タプルとして認識させるためにカンマ
        # 読み取り専用として表示
        read_only_fields = ('email', 'username') 

    def update(self, instance, validated_data):
        # ユーザー情報を更新
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.save()

        return instance



""" カスタムメニューのシリアライザ """
class CustomMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMenu
        fields = '__all__'
