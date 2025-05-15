from django.urls import path
from .views import (
    UserRegisterView,
    UserProfileView,
    LogoutView,
    ChangePasswordView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import MyAuctionsView, MyBidsView


app_name = "users"

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('misSubastas/', MyAuctionsView.as_view(), name='user-auctions'),
    path('misPujas/', MyBidsView.as_view(), name='user-bids'),
]
