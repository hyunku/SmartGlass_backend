import boto3
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from home.models import Building
from listapp.serializers import BuildingSerializer
from home.models import Glass
from listapp.serializers import GlassSerializer
from listapp.serializers import ConnectSerializer


# objects.get : 고유한 값(ex:pk)으로 한개의 값만 추출
# objects.filter : 쿼리문으로 데이터를 받아와서 쿼리문으로 작성 가능



class BuildingList(APIView):  # building 목록 보여주기, building 등록
    # 전체 Buillding list를 보여줌
    def get(self, request):
        queryset = Building.objects.all()
        serializer = BuildingSerializer(queryset, many=True)  # many=True : 여러개 객체 serialize 하기 위함
        return Response(serializer.data)


class CreateBuilding(APIView):
    # 새로운 Bulding을 등록
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = BuildingSerializer(data=request.data)
        if serializer.is_valid():  # 유효성 검사
            serializer.save()  # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteBuilding(APIView):
    # Building 객체 가져오기
    def get_object(self, pk):
        try:
            return Building.objects.get(pk=pk)
        except Building.DoesNotExist:
            raise Http404

    # 삭제할 Building의 detail 보기
    def get(self, request, pk, format=None):
        building = self.get_object(pk)
        serializer = BuildingSerializer(building)
        return Response(serializer.data)

    # Building 삭제하기
    def delete(self, request, pk):
        building = self.get_object(pk=pk)
        building.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class GlassList(APIView):
    # 전체 Glass list를 보기
    def get(self, request):
        queryset = Glass.objects.all()
        serializer = GlassSerializer(queryset, many=True)  # many=True : 여러개 객체 serialize 하기 위함
        return Response(serializer.data)

class CreateGlass(APIView):
    # 새로운 Glass를 등록
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = GlassSerializer(data=request.data)
        if serializer.is_valid():  # 유효성 검사
            serializer.save()  # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인 -> 글래스 선택 -> 로그인 유저의 user_id를 글래스의 user_id와 동일하게끔 글래스db 수정 -> 로그아웃시 글래스db의 user_id는 null로
class Connect_user_glass(APIView):
    # glass 객체 가져오기
    def get_object(self, pk):
        try:
            return Glass.objects.get(pk=pk)
        except Glass.DoesNotExist:
            raise Http404

    # 선택한 glass 보기
    def get(self, request, pk, format=None):
        glass = self.get_object(pk)
        serializer = GlassSerializer(glass)
        return Response(serializer.data)

    # user_id 로 선택한 glass 연결
    def put(self, request, pk):
        response_data = {
            "code" : 200,
            "message" : "연결되었습니다."
        }
        glass = self.get_object(pk)
        serializer = ConnectSerializer(glass, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UnConnect_user_glass(APIView):
    # glass 객체 가져오기
    def get_object(self, pk):
        try:
            return glass.objects.get(pk=pk)
        except glass.DoesNotExist:
            raise Http404
    # 선택한 glass 보기
    def get(self, request, pk, format=None):
        glass = self.get_object(pk)
        serializer = GlassSerializer(glass)
        return Response(serializer.data)
    # user_id 에 null이라고 입력해서 연결 해제하기
    def put(self, request, pk):
        response_data = {
            "code": 200,
            "message": "연결 해제되었습니다."
        }
        glass = self.get_object(pk)
        serializer = ConnectSerializer(glass, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

