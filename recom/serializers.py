from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from .models import *
from accounts.models import *
from map.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id','nickname','profile']

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id','nickname']

class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model=Map
        fields = ['id','name']

class AlertSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    map = serializers.SerializerMethodField()

    class Meta:
        model = Alert
        fields = ['id', 'type', 'user', 'map', 'created_at']

    def get_id(self, obj):
        return obj.recommend.pk
    def get_user(self, obj):
        return UserSerializer(obj.viewuser).data
    def get_map(self, obj):
        map=get_object_or_404(Map,id= obj.recommend.map.id)
        return MapSerializer(map).data
class AlertCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields='__all__'


class ReactSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer()
    mine = serializers.SerializerMethodField()
    class Meta:
        model=React
        fields = ['emoji','content','user','mine']
    def get_mine(self, obj):
        request = self.context.get('request')
        if obj.recommend.map.user.id == request.user.id:
            return True
        return False
    
class ReactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=React
        fields = '__all__'

class HashtagNameSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hashtag
        fields = ['tagname']

class MapSerializer(serializers.ModelSerializer):
    hashtag = HashtagNameSerializer(many=True)
    recom_num = serializers.SerializerMethodField()
    class Meta:
        model = Map
        fields = ['id', 'name', 'location', 'img', 'user', 'hashtag', 'recom_num']

    def get_recom_num(self, obj):
        map_id = obj.id
        recom_num = Recommend.objects.filter(map=map_id).count()
        return recom_num
class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"

class ReactminiSerializer(serializers.ModelSerializer):
    class Meta:
        model=React
        fields = ['id','emoji','content','user']

class RecommendDetailSerializer(serializers.ModelSerializer):
    hashtag = HashtagNameSerializer(many=True)
    place=PlaceSerializer(many=True)
    # react=ReactminiSerializer(source='recom_map')
    nickname=serializers.SerializerMethodField()
    class Meta:
        model = Recommend
        fields=['id','title','content','nickname','hashtag','place']
    def get_nickname(self, obj):
        return obj.user.nickname
    
class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommend
        fields = "__all__"
