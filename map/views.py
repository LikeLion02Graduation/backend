from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.db.models import Count
# Create your views here.

class MapView(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        hashtags = request.data['hashtag']
        request.data['user'] = request.user.id
        request=request.data
        request.pop('hashtag')
        serializer = MapCreateSerializer(data=request)

        if serializer.is_valid():
            newmap=serializer.save()
            for hashtag in hashtags:
                hashtagID = get_object_or_404(Hashtag, tagname=hashtag).id
                newmap.hashtag.add(hashtagID)
            return Response({'message':'내 지도 생성 성공','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message':'내 지도 생성 실패','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        order= request.GET.get('order')
        userID=request.user.id
        if order=="추천순":
            maps_list = Map.objects.filter(user=userID)
            maps = maps_list.annotate(recommend_count=Count('recom_map')).order_by('-recommend_count')
        else:
            maps = Map.objects.filter(user=userID).order_by('-created_at')
        serializer = MapListSerializer(maps, many=True)
        return Response({'message':'내 지도 list 조회 성공','data':serializer.data},status=status.HTTP_200_OK)
    def patch(self,request):
        # request.data['user'] = request.user.id
        # if 'hashtag' in request.data:
        #     hashtags = request.data['hashtag']
        # request=request.data
        # request.pop('hashtag')
        # serializer = MapCreateSerializer(data=request)
        mapid = request.data['id']
        map = get_object_or_404(Map, id=mapid)
        for key, value in request.data.items():
            if key == "hashtag":
                map.hashtag.clear()
                for hashtag in value:
                    hashtagID = get_object_or_404(Hashtag, tagname=hashtag).id
                    map.hashtag.add(hashtagID)
            else:
                setattr(map, key, value)
        map.save()
        serializer = MapCreateSerializer(map)
        return Response({'message':'내 지도 수정 성공','data':serializer.data},status=status.HTTP_200_OK)


class MyBuyMapView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        order= request.GET.get('order')
        user=request.user
        all_maps = Map.objects.all()
        maps_list = all_maps.filter(buyers=user.pk)
        if order=="추천순":
            maps = maps_list.annotate(recommend_count=Count('recom_map')).order_by('-recommend_count')
        else:
            maps = maps_list.order_by('-created_at')
        serializer = MapListSerializer(maps, many=True)
        return Response({'message':'구매한 지도 list 조회 성공','data':serializer.data},status=status.HTTP_200_OK)
