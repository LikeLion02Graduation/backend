from django.contrib import admin
from django.urls import path
from .views import *

app_name='recom'      

urlpatterns = [
    path('notice/',AlertView.as_view()),
    path('notice/<int:pk>',AlertDeleteView.as_view()),
    path('react/<int:pk>',ReactView.as_view()),
    path('content/',OtherMapsView.as_view()),
]