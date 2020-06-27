from django.urls import path
from .views import SignupUser, SignupCollaborator, PageGeneratingOTPView, SigninCollaborator, SigninUser
from . import views


app_name = 'user'
urlpatterns = [
    path('phone_number/', PageGeneratingOTPView.as_view(), name="generating_otp"),
    path('signup/<str:phone>/user',  SignupUser.as_view(),  name="signup_user"),
    path('signup/<str:phone>/collaborator', SignupCollaborator.as_view(),  name="signup_collaborator"),
    path('signin/<str:phone>/collaborator',  SigninCollaborator.as_view(),  name="signin_collaborator"),
    path('signin/<str:phone>/user',  SigninUser.as_view(),  name="signin_user"),
    path('logout/',  views.user_logout, name="logout"),
]
