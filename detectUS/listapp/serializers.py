from rest_framework import serializers

from home.models import Building, Company


class CompanySerializer(serializers.Serializer):
    class Meta:
        model = Company
        fields = ['company_id', 'company_name']


class BuildingSerializer(serializers.ModelSerializer):
    company_name = CompanySerializer()

    class Meta:
        model = Building
        fields = '__all__'