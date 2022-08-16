from rest_framework import serializers

from home.models import Building, Company, Glass, Issue, Raw_data

from rest_framework.serializers import ModelSerializer

from home.models import Issue, Raw_data, Drawing


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
        fields = ['glass_name']


class ShowUserBuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['building_id', 'building_name', 'building_context']


class BuildingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['building_name', 'max_floor', 'min_floor', 'building_context', 'company_id']


class RawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raw_data
        fields = ['picture']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['floor', 'room', 'details', 'raw_data_id']


class BuildingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['building_name', 'max_floor', 'min_floor']


class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = ['drawing']

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['Building'] = ShowUserBuildingSerializer(instance.company_id).data
    #     return response
