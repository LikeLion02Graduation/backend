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


