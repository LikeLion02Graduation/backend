from django.contrib import admin
from django.urls import path,include
from .views import *

app_name='accounts'      

urlpatterns = [
    path('kakao/', KakaoLoginView.as_view()),
    path('kakao/callback/',KakaoCallbackView.as_view()),
    path('signup/',SignUpView.as_view()),
    path('signin/',LoginView.as_view()),
    path('kakao/edit/',MyProfileView.as_view()),
    path('del/',DelUserView.as_view()),
    path('duplicate/',DuplicateIDView.as_view())
]
