from rest_framework import serializers

from home.models import Building, Company

from home.models import glass

from home.models import account


class CompanySerializer(serializers.Serializer):
    class Meta:
        model = Company
        fields = '__all__'


class BuildingSerializer(serializers.ModelSerializer):
    company_id_imsi = CompanySerializer(read_only=True)
    class Meta:
        model = Building
        fields = '__all__'


class BuildingTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['company_id'] = CompanySerializer(instance.company_id).data
        return response


class GlassSerializer(serializers.ModelSerializer):
    class Meta:
        model = glass
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = ['user_id', 'company_id', 'is_admin', 'name']


class ConnectSerializer(serializers.ModelSerializer):
    user_id_imsi = AccountSerializer(read_only=True)
    class Meta:
        model = glass
        fields = '__all__'

# 유저 테이블에서 유저 아이디를 참고해서