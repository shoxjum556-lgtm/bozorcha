from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenBlacklistView,
)

from .views import RegisterView, ProfileDetailView

urlpatterns = [
    # login and register
    path('register/', RegisterView.as_view(), name="register"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),

    # Profile
    path('profile/', ProfileDetailView.as_view(), name="profile"),
]
