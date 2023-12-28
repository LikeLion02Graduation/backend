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
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model=Map
        fields = ['user','name','location','hashtag','img','description','buyers','created_at']

class MapListSerializer(serializers.ModelSerializer):
    hashtag=HashtagNameSerializer(many=True)
    recommend_num = serializers.SerializerMethodField()
    react_num = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model=Map
        fields = ['id','user','name','location','hashtag','img','description','created_at','recommend_num','react_num']
    def get_recommend_num(self, obj):
        mapID=obj.id
        recommendsNum = Recommend.objects.filter(map=mapID).count()
        return recommendsNum
    def get_react_num(self, obj):
        mapID = obj.id
        count=0
        recommends = Recommend.objects.filter(map=mapID)
        for recommend in recommends:
            recomID=recommend.id
            count+=React.objects.filter(recommend=recomID).count()
        return count
    
class MapPatchSerializer(serializers.ModelSerializer):
    hashtag = HashtagNameSerializer(many=True)

    class Meta:
        model = Map
        fields = ['id', 'name', 'location', 'img', 'description', 'hashtag']

    def create(self, validated_data):
        hashtag_data = validated_data.pop('hashtag', [])
        map_instance = Map.objects.create(**validated_data)

        for hashtag in hashtag_data:
            tagname = hashtag.get('tagname')
            hashtag_obj, created = Hashtag.objects.get_or_create(tagname=tagname)
            map_instance.hashtag.add(hashtag_obj)

        return map_instance