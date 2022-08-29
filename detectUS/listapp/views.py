import boto3
from django.http import Http404, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from home.models import Building, Glass, Account, Issue, Raw_data, Floor
from listapp.serializers import BuildingSerializer, GlassSerializer, ShowUserBuildingSerializer, \
    BuildingCreateSerializer, DrawingSerializer


# objects.get : 고유한 값(ex:pk)으로 한개의 값만 추출 -> obj 형태로 받음
# objects.filter : 쿼리문으로 데이터를 받아와서 쿼리문으로 작성 가능 -> queryset 형태로 받음
# objects.filter() : queryset 객체 자체가 나옴
# objects.filter().values() : queryset 객체 내부 특정 속성들까지 출력시켜줌


# <참조와 역참조>

# 내 모델 안에 지정한걸 볼 때는 정참조
# 나를 지정한 놈을 볼 때는 역참조

# query셋으로 받을 때 사용 가능
# many-to-many(N->N), one-to-many(1->N)가 prefetch_related 사용 -> 역참조
# many-to-one(N->1), one-to-one(1->1)가 select_related 사용 -> 정참조

# <serilaizer 내부 객체에 접근하는 3가지 방법>

# 단, serializer 객체를 정의하면서 serializer = serializer클래스(data=request.data) 처럼 request.data 정의되어야 사용가능

# 1. initial_data - 유효성 검사를 하기 전에 필드에 접근할 수 있다.
# seirlaizer.initial_data['필드'] = 값

# 2. validated_data - 유효성 검사를 통과한 필드에 접근을 할 수 있다.
# if serializer.is_valid():
#     serializer.validated_data['필드'] = 값
#     serializer.save()

# 3. data - 유효성 검사를 통과하고 save된 필드에 접근할 수 있다.
# if serializer.is_valid():
#     serializer.save()
#     serializer.data['필드']

class BuildingDetail(APIView):  # 특정 빌딩 관련 전체 데이터들
    def get_object(self, pk):
        try:
            return Building.objects.get(pk=pk)
        except Building.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        # queryset load
        building = Building.objects.filter(building_id=pk).values("building_name", "max_floor", "min_floor")
        rawdataID = Raw_data.objects.filter(upload_target_building_id=pk).values("raw_data_id")
        pict = Raw_data.objects.filter(upload_target_building_id=pk).values("picture")

        rawdataID_list = []  # 1,3 저장됨.
        for qs in rawdataID.values():
            rawdataID_list.append(qs['raw_data_id'])
        issue = Issue.objects.filter(raw_data_id__in=rawdataID_list).values("raw_data_id", "floor", "room", "details")

        # queryset -> list
        pict_list = [x for x in pict]
        issue_list_imsi = [x for x in issue]

        # many list -> one dict -> one list
        issue_list = [dict(i, **j) for i, j in zip(issue_list_imsi, pict_list)]

        # drawing 데이터 리턴
        drawings = Floor.objects.filter(building_id=pk).values("drawing")  # queryset load
        drawings_list = [x for x in drawings]  # queryset -> list
        drawing_list = []  # 보여줄 값들 리스트

        # 쿼리셋의 중괄호들 없애기
        for i in range(len(drawings_list)):
            drawing_list.append(drawings_list[i]['drawing'])

        response_data = {
            "building_name": building[0]['building_name'],
            "max_floor": building[0]['max_floor'],
            "min_floor": building[0]['min_floor'],
            "drawing_list": drawing_list,
            "issue_list": issue_list}

        return Response(response_data)


class ShowUserBuilding(APIView):  # 로그인한 유저의 user_id 를 받아와서 유저에 해당하는 건물들 출력
    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except Building.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        account = self.get_object(pk)  # 로그인한 유저의 Account DB 정보
        company = account.company_id  # 로그인 유저의 company_id 들 가져오기
        buildings = company.building_set.all()  # 역참조 데이터 읽기 - 테이블에 related_name 설정 안되어있을 때 - 테이블명소문자_set 사용
        serializer = ShowUserBuildingSerializer(buildings, many=True)
        print(serializer.data)
        return Response({"admin": account.is_admin,
                         "building_list": serializer.data})


# 빌딩 등록 시 building_name, max min floor, building_context만 받아오게끔 -> company_id 는 user_id -> company_id 로 받아오게끔
class CreateBuilding(APIView):  # 빌딩 등록
    # 새로운 Bulding을 등록
    def post(self, request, pk):
        account = Account.objects.get(pk=pk)  # user_id로 Account table 전달
        company = account.company_id  # Account table의 company_id로 Company 정참조 (Account 테이블의 fk(N) -> Company 테이블의 pk(1))
        if account.is_admin == 1:  # 관리자만 빌딩 등록 가능
            # request.data는 사용자의 입력 데이터
            serializer = BuildingCreateSerializer(data=request.data)
            serializer.initial_data['company_id'] = company.company_id  # Serializer의 key값(company_id)과 value값으로 참조한 user_id로부터 참조한 company_id 입력
            if serializer.is_valid():  # 유효성 검사
                serializer.save()  # 저장
                return Response({"message" : "빌딩이 생성되었습니다.",
                                 "생성한 building_id" : serializer.data["building_id"]})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"adminerror": "관리자가 아닙니다"})


class DeleteBuilding(APIView):  # 빌딩 삭제
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


class CreateGlass(APIView):
    # 새로운 Glass를 등록
    def post(self, request, pk):
        response_data = {
            "code": 200,
            "message": "생성되었습니다."
        }
        account = Account.objects.get(pk=pk)  # user_id로 Account table 전달
        if account.is_admin == 1:
            # request.data는 사용자의 입력 데이터
            serializer = GlassSerializer(data=request.data)
            if serializer.is_valid():  # 유효성 검사
                serializer.save()  # 저장
                return Response(response_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"adminerror": "관리자가 아닙니다"})


def show_glass_list2(request, user_id):
    # 접속 user의 company에서 관리하는 glass만 선택
    user_company = Account.objects.filter(user_id__exact=user_id).values('company_id')
    glass = Glass.objects.filter(company_id__exact=user_company[0]['company_id']).values('glass_id', 'glass_name',
                                                                                         'user_id', 'building_id')

    # Queryset을 python list로 변환
    glass_list = [entry for entry in glass]

    # building_id와 user_id를 이용하여 building_name과 user_name 추출
    for i in range(len(glass_list)):
        user_name = Account.objects.filter(user_id__exact=glass_list[i]['user_id']).values('name')
        building_name = Building.objects.filter(building_id__exact=glass_list[i]['building_id']).values('building_name')

        if not building_name and not user_name:
            glass_list[i]['building_name'] = None
            glass_list[i]['user_name'] = None
        else:
            glass_list[i]['building_name'] = building_name[0]['building_name']
            glass_list[i]['user_name'] = user_name[0]['name']

    # enable 설정, user_id가 None이면 enable=0, else enable=1
    for i in range(len(glass_list)):
        if glass_list[i]['user_id'] is None:
            glass_list[i]['enable'] = 0
        else:
            glass_list[i]['enable'] = 1

    # list에서 불필요한 data(user_id,building_id) 제거
    for i in range(len(glass_list)):
        del (glass_list[i]['user_id'])
        del (glass_list[i]['building_id'])

    # 최종 보낼 data
    data = {"admin": 1, "glass_list": glass_list}

    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
