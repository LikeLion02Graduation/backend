from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import *
from django.db.models import Count
from map.models import *
# Create your views here.



class AlertView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        userID=request.user.id
        alerts = Alert.objects.filter(user=userID).order_by('-created_at')
        
        serializer = AlertSerializer(alerts, many=True)
        return Response({'message':'알림 조회 성공','data':serializer.data},status=status.HTTP_200_OK)

class AlertDeleteView(views.APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,pk):
        alert = get_object_or_404(Alert, id=pk)
        
        if request.user != alert.user:
            return Response({'message': '이 알림을 지울 권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)

        # Perform the delete operation
        alert.delete()

        return Response({'message':'알림 삭제 성공'},status=status.HTTP_200_OK)
    

class ReactView(views.APIView):
    def get(self,request,pk):
        try:
            react=get_object_or_404(React,recommend=pk)
            serializer = ReactSerializer(react,context={'request': request})
            return Response({'message':'추천 반응 조회 성공','data':serializer.data},status=status.HTTP_200_OK)
        except:
            recom=get_object_or_404(Recommend,id=pk)
            if recom.map.user.id == request.user.id: mapmine=True
            else: mapmine=False
            return Response({'message':'추천 반응이 없습니다',"data":{"mine":mapmine}},status=status.HTTP_200_OK)
    def post(self,request,pk):
        recom=get_object_or_404(Recommend,id=pk)
        request.data['recommend']=pk
        request.data['user'] = request.user.id
        serializer=ReactCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            alert_data={
                "user":recom.user.id,
                "recommend":pk,
                "viewuser":request.user.id,
                "type":"반응"
            }
            alertSerializer=AlertCreateSerializer(data=alert_data)
            if alertSerializer.is_valid():
                alertSerializer.save()
            return Response({'message':'추천 반응 남기기 성공','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message':'추천 반응 남기기 실패','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    def patch(self,request,pk):
        # request.data['recommend']=pk
        # request.data['user'] = request.user.id

        # recom=get_object_or_404(Recommend,id=pk)
        react = get_object_or_404(React, recommend=pk)
        self.check_object_permissions(self.request, react)
        for key, value in request.data.items():
            setattr(react, key, value)
        react.save()
        serializer = ReactCreateSerializer(react)
        return Response({'message':'추천 반응 수정 성공','data':serializer.data},status=status.HTTP_200_OK)

class OtherMapsView(views.APIView):
    def get(self,request):
        key= request.GET.get('key')
        maps=Map.objects.filter(location=key).order_by('-created_at')
        serializers = MapSerializer(maps,many=True)
        return Response({'message':'추천 콘텐츠 list 조회 성공','data':serializers.data},status=status.HTTP_200_OK)

class RecommendDetailView(views.APIView):
    def get(self,request,pk):
        recom=get_object_or_404(Recommend,id=pk)
        serializer = RecommendDetailSerializer(recom)
        return Response({'message':'추천 상세 조회 성공','data':serializer.data},status=status.HTTP_200_OK)
    def delete(self,request,pk):
        recom=get_object_or_404(Recommend,id=pk)
        recom.delete()
        return Response({'message':'추천 삭제 성공'},status=status.HTTP_200_OK)
    
class RecommendCreateView(views.APIView):
    def post(self,request):
        data = request.data

        map = data.get('map_id')
        mapObj = Map.objects.get(id=map)
        title = data.get('title')
        content = data.get('content')
        user = request.user.id
        
        places_data = data.get('place', [])
        hashtags_data = data.get('hashtag', [])

        recommend = Recommend.objects.create(
                user_id=user,
                map=mapObj,
                title=title,
                content=content
            )

        for place_data in places_data:
                place, created = Place.objects.get_or_create(
                    name=place_data['name'],
                    address=place_data['address'],
                    link=place_data['link']
                )
                recommend.place.add(place)
        for hashtag in hashtags_data:
                hashtag = get_object_or_404(Hashtag,tagname=hashtag)
                recommend.hashtag.add(hashtag)
        serializer = RecommendSerializer(recommend)
        
        alert_data={
            "user": mapObj.user.id,
            "recommend":recommend.id,
            "viewuser":request.user.id,
            "type":"추천"
        }
        alertSerializer=AlertCreateSerializer(data=alert_data)
        if alertSerializer.is_valid():
            alertSerializer.save()
            return Response({'message': '추천 작성 성공', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message':'추천 작성 실패','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

