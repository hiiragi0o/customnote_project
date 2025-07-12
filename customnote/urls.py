from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


urlpatterns = [
    # ユーザー認証用
    path('signup/', views.UserCreateAPIView.as_view(), name='signup'),
    path('me/', views.UserInfoAPIView.as_view(), name='user_info'),
    path('me/update/', views.UserUpdateAPIView.as_view(), name='user_update'),
    path('me/delete/', views.UserDeleteAPIView.as_view(), name='user_delete'),

    # JWT認証用
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # アプリのURL
    path('notes/<int:pk>/', views.CustomMenuDetailView.as_view(), name='custom_menu_detail'),
    path('', views.HomeView.as_view(), name='home'),
]
