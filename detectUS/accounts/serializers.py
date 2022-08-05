from rest_framework import serializers
from home.models import account


class signupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = account
        fields = '__all__'#'[__all__]' 아님 
 

class loginSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = ['user_id', 'user_pw']
"""
class logoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = '__all__'#'[__all__]' 아님 
"""