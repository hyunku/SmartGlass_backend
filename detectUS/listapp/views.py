from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from home.models import Building
from listapp.serializers import BuildingSerializer


class BuildingList(APIView):
    # Buillding list를 보여줄 때
    def get(self, request):
        buildings = Building.objects.all()
        # 여러 개의 객체를 serialization하기 위해 many=True로 설정
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)

    # 새로운 Bulding을 등록할 때
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = BuildingSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
