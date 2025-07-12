""" DRF用のユーザー認証に関するビューを定義 """
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser, CustomMenu
from .serializers import CustomUserSerializer, UserUpdateSerializer, CustomMenuSerializer

""" Djangoのビューをインポート """
from django.views.generic import View
from django.shortcuts import render



""" ホームビューを定義 """
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'templates/customnote/home.html')



""" ユーザー認証に関するAPIビューを定義 """
# ユーザー登録APIビュー
class UserCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny] # 認証なしでアクセスを許可 (新規登録のため)


# ユーザー情報取得APIビュー
class UserInfoAPIView(APIView):
    permission_classes = [IsAuthenticated] # 認証されたユーザーのみがアクセスできるように設定

    def get(self, request):
        # 認証されたユーザーの情報を取得
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


# ユーザー情報更新APIビュー
class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all() # ユーザーオブジェクトをクエリするためのクエリセット
    serializer_class = UserUpdateSerializer # 更新用のUserUpdateSerializerを使用
    permission_classes = [IsAuthenticated] # 認証済みユーザーのみアクセス可能

    def get_object(self):

        return self.request.user

    def update(self, request, *args, **kwargs):
        # PATCHリクエストの場合、部分更新を許可する
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 更新後のユーザー情報をUserSerializerで返却
        response_serializer = CustomUserSerializer(instance) 

        return Response(response_serializer.data)


# アカウント削除APIビュー
class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all() # ユーザーオブジェクトをクエリするためのクエリセット
    permission_classes = [IsAuthenticated] # 認証済みユーザーのみアクセス可能

    def get_object(self):

        return self.request.user

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({"message": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


""" カスタムノートに関するAPIビューを定義 """
class CustomMenuDetailView(generics.RetrieveAPIView):
    queryset = CustomMenu.objects.all()
    serializer_class = CustomMenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # 認証済みユーザーのみアクセス可能
