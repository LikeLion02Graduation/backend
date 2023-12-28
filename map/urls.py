from django.contrib import admin
from django.urls import path
from .views import *

app_name='map'      

urlpatterns = [
    path('', MapView.as_view()),
    path('others',MyBuyMapView.as_view())
]