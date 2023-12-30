from django.shortcuts import render,redirect
from django.http import JsonResponse
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import MyMap
import requests
from .models import *
from .serializers import *
import json
from rest_framework.permissions import IsAuthenticated


from rest_auth.registration.views import SocialLoginView                   
# from allauth.socialaccount.providers.kakao import views as kakao_views     
from allauth.socialaccount.providers.oauth2.client import OAuth2Client  
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter



# Create your views here.

BASE_URL = 'http://127.0.0.1:8000/'

KAKAO_CONFIG = {
    "KAKAO_REST_API_KEY":getattr(MyMap.settings.base, 'KAKAO_CLIENT_ID', None),
    "KAKAO_REDIRECT_URI": f"{BASE_URL}accounts/kakao/callback/",
    "KAKAO_CLIENT_SECRET_KEY": getattr(MyMap.settings.base, 'KAKAO_CLIENT_SECRET_KEY', None), 
    "KAKAO_PW":getattr(MyMap.settings.base, 'KAKAO_PW', None),
}
kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"


class KakaoLoginView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        '''
        kakao code 요청
        '''
        client_id = KAKAO_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = KAKAO_CONFIG['KAKAO_REDIRECT_URI']

        uri = f"{kakao_login_uri}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        
        res = redirect(uri)
        # res = requests.get(uri)
        print(res.get("access_tocken"))
        return res
    

class KakaoCallbackView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request):         # kakao access_token 요청 및 user_info 요청
        data = request.query_params.copy()

        # access_token 발급 요청
        code = data.get('code')
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request_data = {
            'grant_type': 'authorization_code',
            'client_id': KAKAO_CONFIG['KAKAO_REST_API_KEY'],
            'redirect_uri': KAKAO_CONFIG['KAKAO_REDIRECT_URI'],
            'client_secret': KAKAO_CONFIG['KAKAO_CLIENT_SECRET_KEY'],
            'code': code,
        }
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        token_res = requests.post(kakao_token_uri, data=request_data, headers=token_headers)

        token_json = token_res.json()
        access_token = token_json.get('access_token')

        if not access_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        access_token = f"Bearer {access_token}" \

        # kakao 회원정보 요청
        auth_headers = {
            "Authorization": access_token,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        user_info_res = requests.get(kakao_profile_uri, headers=auth_headers)
        user_info_json = user_info_res.json()

        social_type = 'kakao'
        social_id = f"{social_type}_{user_info_json.get('id')}"

        properties = user_info_json.get('properties')
        nickname=properties.get('nickname')
        profile=properties.get('thumbnail_image_url')
        print(user_info_json)

        # 회원가입 및 로그인 처리 
        try:   
            user_in_db = User.objects.get(username=social_id) 
            # kakao계정 아이디가 이미 가입한거라면
            # 서비스에 rest-auth 로그인
            data={'username':social_id,'password':social_id}
            serializer = UserLoginSerializer(data=data)
            if serializer.is_valid():
                return Response({'message': "카카오 로그인 성공", 'data': serializer.validated_data}, status=status.HTTP_200_OK)
            return Response({'message': "카카오 로그인 실패", 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:   
            # 회원 정보 없으면 회원가입 후 로그인
            # def post(self,request):
            print("회원가입")
            data={'username':social_id,'password':social_id,'nickname':nickname,'profile':profile}
            serializer=SignUpSerializer(data=data)  
            if serializer.is_valid():
                serializer.save()                          # 회원가입
                data1={'username':social_id,'password':social_id}
                serializer1 = UserLoginSerializer(data=data1)
                if serializer1.is_valid():
                    return Response({'message':'카카오 회원가입 성공','data':serializer1.validated_data}, status=status.HTTP_201_CREATED)
            return Response({'message':'카카오 회원가입 실패','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    


# class KakaoToDjangoLogin(SocialLoginView):
#     adapter_class = KakaoOAuth2Adapter
#     callback_url = KAKAO_CONFIG['KAKAO_REDIRECT_URI']
#     client_class = OAuth2Client
        
class SignUpView(views.APIView):
    def post(self,request):
        serializer=SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()               
            return Response({'message':'회원가입 성공','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message':'회원가입 실패','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    
class LoginView(views.APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': "로그인 성공", 'data': serializer.validated_data}, status=status.HTTP_200_OK)
        return Response({'message': "로그인 실패", 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

       
class MyProfileView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response({'message': '카카오 로그인 완료, 이름 바꾸기 페이지', 'data': serializer.data}, status=status.HTTP_200_OK)
    def patch(self, request):
        serializer = UserProfileSimpleSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '정보 변경 성공', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': '유효하지 않은 데이터입니다.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

