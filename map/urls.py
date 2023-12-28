from django.contrib import admin
from django.urls import path
from .views import *

app_name='map'      

urlpatterns = [
    path('', MapView.as_view()),
    path('edit/',MapPatchView.as_view()),
    path('others/',MyBuyMapView.as_view()),
    path('detail/<int:pk>/',MapDetailView.as_view()),
    path('newtag/',NewTagView.as_view()),
]