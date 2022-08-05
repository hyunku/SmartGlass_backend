from rest_framework import serializers

from home.models import Building, Company

from home.models import Glass

from home.models import Account


class CompanySerializer(serializers.Serializer):
    class Meta:
        model = Company
        fields = '__all__'


class BuildingSerializer(serializers.ModelSerializer):
    company_id_imsi = CompanySerializer(read_only=True)
    class Meta:
        model = Building
        fields = '__all__'


class GlassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glass
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'company_id', 'is_admin', 'name']


class ConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glass
        fields = ['user_id']

