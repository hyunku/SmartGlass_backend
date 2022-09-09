from rest_framework import serializers

from home.models import Building, Company, Glass, Issue, Raw_data, Floor

from rest_framework.serializers import ModelSerializer



class CompanySerializer(serializers.Serializer):
    class Meta:
        model = Company
        fields = ['company_id']


class BuildingSerializer(serializers.ModelSerializer):
    company_id_imsi = CompanySerializer(read_only=True)

    class Meta:
        model = Building
        fields = '__all__'


class GlassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glass
        fields = ['glass_name', 'company_id']


class ShowUserBuildingSerializer(serializers.ModelSerializer):
    # 1. 추가 or 수정하고 싶은 속성 정의 - read_only용도
    name = serializers.SerializerMethodField()
    context = serializers.SerializerMethodField()

    # 3. fields 에 리턴할 딕셔너리 입력
    class Meta:
        model = Building
        fields = ['building_id', 'name', 'context']

    # 2. get_속성명 으로 시리얼라이저 내부 키/값 수정
    def get_name(self, obj):
        return obj.building_name

    def get_context(self, obj):
        return obj.building_context


# serializers의 필드명 변경하기 - 저장, 출력 모두 가능
class BuildingCreateSerializer(serializers.ModelSerializer):
    context = serializers.CharField(source="building_context")

    class Meta:
        model = Building
        fields = ['building_id', 'building_name', 'max_floor', 'min_floor', 'context', 'company_id']


class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['floor', 'building_id', 'drawing']




