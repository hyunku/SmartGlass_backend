from urllib import response
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from home.models import Account
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status

 
class passwordAPIView(APIView):
  
    def put(self, request,user_name):
        response_data = {
        "code": 200,
        "message": "비밀번호 변경에 성공하였습니다."
        }
        user_object = Account.objects.get(user_id=user_name)
        update_user_serializer = passwordSerializer(user_object, data=request.data)
        if update_user_serializer.is_valid():
            update_user_serializer.save()
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        
    #(self, request, *args, **kwargs): 가 아니라 user로 받아야함 , str에서 user로 받아왔기 때문에 *args,**kwargs로 나누어 받으면 model의 주소가 나오게됌
    def get(self, request,user_name):
        queryset = Account.objects.all() #모든 js쿼리셋 데이터 불러옴
     #   print(queryset)
     
        vary=Account.objects.filter(user_id=user_name)# account에서 데이터에 맞는 user필터링하여 가져옴 
     #   print(user_name)
     #   print(vary)
      # many=True의 역할은 쿼리셋이 여러 값으로 이루어진 것이라는 것을 Serializer에게 알려주는 것
        serializer = passwordSerializer(vary, many=True)
        #many true 없애면 에러 생김 
     #   print(serializer.data)
        return Response(serializer.data)
    
class userAPIView(APIView):
    
    def get(self, request,user_name):
        print(user_name)
        queryset = Account.objects.all() 
        vary=Account.objects.filter(user_id=user_name)
        serializer = userchangeSerializer(vary, many=True)
        return Response(serializer.data)
    
    def put(self, request,user_name):
        response_data ={
        "code": 200,
        "message": "사용자 정보 변경에 성공하였습니다."
        }
        user_object = Account.objects.get(user_id=user_name)
        update_user_serializer = userchangeSerializer(user_object, data=request.data)
        if update_user_serializer.is_valid():
            update_user_serializer.save()
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
    