from django.contrib import admin
from django.urls import path,include
from .views import *

app_name='accounts'      

urlpatterns = [
    path('kakao/', KakaoLoginView.as_view()),
    path('kakao/callback/',KakaoCallbackView.as_view()),
]