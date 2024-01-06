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

class HashtagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hashtag
        fields = '__all__'

class HashtagNameSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hashtag
        fields = ['tagname']

class RecommendSimpleSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    mine = serializers.SerializerMethodField()
    class Meta:
        model=Hashtag
        fields = ['id','user','mine']
    def get_mine(self, obj):
        request = self.context.get('request')
        if obj.user == request.user:
            return True
        return False

class MapListSerializer(serializers.ModelSerializer):
    hashtag=HashtagNameSerializer(many=True)
    recommend_num = serializers.SerializerMethodField()
    react_num = serializers.SerializerMethodField()
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
            hashtag_obj = get_object_or_404(Hashtag,tagname=tagname)
            map_instance.hashtag.add(hashtag_obj)

        return map_instance
    
class MapDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    hashtag = HashtagNameSerializer(many=True)
    buyers = UserSerializer(many=True)
    map_mine = serializers.SerializerMethodField()
    do_buy = serializers.SerializerMethodField()
    recommend_num = serializers.SerializerMethodField()
    recommend = RecommendSimpleSerializer(many=True, source='recom_map')

    class Meta:
        model = Map
        fields = ['id', 'name', 'location', 'hashtag', 'img', 'description', 'created_at', 'buyers', 'user',
                  'map_mine', 'do_buy', 'recommend_num', 'recommend']

    def get_map_mine(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.user == request.user
        return False

    def get_do_buy(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return request.user in obj.buyers.all()
        return False

    def get_recommend_num(self, obj):
        map_id = obj.id
        recommends_num = Recommend.objects.filter(map=map_id).count()
        return recommends_num

    def get_react_num(self, obj):
        map_id = obj.id
        count = 0
        recommends = Recommend.objects.filter(map=map_id)
        for recommend in recommends:
            recommend_id = recommend.id
            count += React.objects.filter(recommend=recommend_id).count()
        return count

    def get_recommend(self, obj):
        request = self.context.get('request')
        return RecommendSimpleSerializer(many=True, source='recom_map', context={'request': request})
