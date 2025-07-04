from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignupView,LoginView,LogoutView,UserProfileView,UserProfileEditView,CreateSuperUserAPIView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("logout/",LogoutView.as_view(),name="logout"),
    path('user/',UserProfileView.as_view(),name="user-profile"),
    path('edit/user/',UserProfileEditView.as_view(),name="edit-profile"),
    
    path('create-superuser/', CreateSuperUserAPIView.as_view()),
]
