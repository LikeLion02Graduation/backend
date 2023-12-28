from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from .models import *
from accounts.models import *

class MapCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Map
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id','nickname']

class HashtagNameSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hashtag
        fields = ['tagname']

class HashtagNameSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hashtag
        fields = ['tagname']

class MapSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    hashtag=HashtagNameSerializer(many=True)
    buyers=UserSerializer(many=True)
    class Meta:
        model=Map
        fields = ['user','name','location','hashtag','img','description','buyers','created_at']