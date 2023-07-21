from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import (
    CreateUserView,
    ManageUserView,
    LogOutView,
)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("log_out/", LogOutView.as_view(), name="log_out"),
]

app_name = "user"