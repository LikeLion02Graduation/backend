from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import *
from django.db.models import Count
from .permissions import *
from .storages import FileUpload, s3_client
# Create your views here.

class MapView(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        file = request.FILES.get('img')
        folder = 'map_img'

        request.data.pop('img')

        hashtags = request.data['hashtag']
        request.data['user'] = request.user.id
        request=request.data
        request.pop('hashtag')
        serializer = MapCreateSerializer(data=request)

        if serializer.is_valid():
            file_url = FileUpload(s3_client).upload(file, folder)
            newmap=serializer.save(img=file_url)
            for hashtag in hashtags:
                hashtagID = get_object_or_404(Hashtag, tagname=hashtag).id
                newmap.hashtag.add(hashtagID)
            return Response({'message':'내 지도 생성 성공','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message':'내 지도 생성 실패','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        order= request.GET.get('order')
        userID=request.user.id
        if order=="오래된순":
            maps = Map.objects.filter(user=userID).order_by('created_at')
            # 추천순
            # maps_list = Map.objects.filter(user=userID)
            # maps = maps_list.annotate(recommend_count=Count('recom_map')).order_by('-recommend_count')
        else:
            maps = Map.objects.filter(user=userID).order_by('-created_at')
        serializer = MapListSerializer(maps, many=True)
        return Response({'message':'내 지도 list 조회 성공','data':serializer.data},status=status.HTTP_200_OK)
    
class MapPatchView(views.APIView):
    permission_classes = [IsOwner]
    def patch(self,request):
        mapid = request.data['id']
        map = get_object_or_404(Map, id=mapid)
        self.check_object_permissions(self.request, map)
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
        # if order=="추천순":
        #     maps = maps_list.annotate(recommend_count=Count('recom_map')).order_by('-recommend_count')
        if order=="오래된순":
            maps = maps_list.order_by('created_at')
        else:
            maps = maps_list.order_by('-created_at')
        serializer = MapListSerializer(maps, many=True)
        return Response({'message':'구매한 지도 list 조회 성공','data':serializer.data},status=status.HTTP_200_OK)

class MapDetailView(views.APIView):
    permission_classes = [AllowAny]
    def get(self,request,pk):
        map = get_object_or_404(Map,id=pk)
        serializers = MapDetailSerializer(map,context={'request': request})
        return Response({'message':"내 지도 조회 성공",'data':serializers.data},status=status.HTTP_200_OK)
    
class NewTagView(views.APIView):
    def post(self,request):
        tagname=request.data['tagname']
        data={
            "tagname":tagname,
            "enable":False
        }
        serializers = HashtagCreateSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return Response({'message':'해시태그 생성 요청 성공','data':serializers.data}, status=status.HTTP_201_CREATED)
        return Response({'message':'해시태그 생성 요청 실패','error':serializers.errors},status=status.HTTP_400_BAD_REQUEST)

class cityView(views.APIView):
    def get(self,request):
        city= request.GET.get('city')
        cityList = {"경기도": ["경기도","가평군","고양시","과천시","광명시","광주시","구리시","군포시","김포시","남양주시","동두천시","부천시","성남시","수원시","시흥시","안산시","안성시","안양시","양주시","양평군","여주시","연천군","오산시","용인시","의왕시","의정부시","이천시","파주시","평택시","포천시","하남시","화성시"],
                    "경상북도": ["경상북도","포항시","경주시","김천시","안동시","구미시","영주시","영천시","상주시","문경시","경산시","군위군","의성군","청송군","영양군","영덕군","청도군","고령군","성주군","칠곡군","예천군","봉화군","울진군","울릉군"],
                    "경상남도": ["경상남도","창원시","진주시","통영시","사천시","김해시","밀양시","거제시","양산시","의령군","함안군","창녕군","고성군","남해군","하동군","산청군","함양군","거창군","합천군"],
                    "충청북도": ["충청북도","청주시", "충주시", "제천시", "보은군", "옥천군", "영동군", "증평군", "진천군", "괴산군", "음성군","단양군"],
                    "충청남도": ["충청남도","천안시", "공주시", "보령시", "아산시", "서산시", "논산시", "계룡시", "당진시", "금산군", "부여군", "서천군", "청양군", "홍성군", "예산군", "태안군"],
                    "전라북도":["전라북도","전주시", "군산시", "익산시", "정읍시", "남원시", "김제시", "완주군", "진안군", "무주군", "장수군", "임실군", "순창군", "고창군", "부안군"],
                    "전라남도":["전라남도","목포시", "여수시", "순천시", "나주시", "광양시", "담양군", "곡성군", "구례군", "고흥군", "보성군", "화순군", "장흥군", "강진군", "해남군", "영암군", "무안군", "함평군", "영광군", "장성군", "완도군", "진도군", "신안군"],
                    "강원도":["강원도","춘천시", "원주시", "강릉시", "동해시", "태백시", "속초시", "삼척시", "홍천군", "횡성군", "영월군", "평창군", "정선군", "철원군", "화천군", "양구군", "인제군", "고성군", "양양군"],
                    "제주":["제주","제주시", "서귀포시"]
                    }
        result = {"city": city, "cities": cityList[city]}
        return Response({'message': '도시 조회 성공', 'data': result}, status=status.HTTP_200_OK)
