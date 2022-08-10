import json
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from home.models import account,Company
from .serializers import companySerializer, signupSerializer

#create
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

# Create your views here.
class signupAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = signupSerializer
   
    def get(self, request,*args, **kwargs):
        queryset = account.objects.all() 
        print(queryset)
        serializer = signupSerializer(many=True)
        return Response(serializer.data)

    
    
    def post(self, request,*args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
        extra_kwargs = {
        'user_id': {
            'validators': [UniqueValidator(queryset=User.objects.all())]
        },
        }


        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response(data=serializer.data, status=400)
    
  