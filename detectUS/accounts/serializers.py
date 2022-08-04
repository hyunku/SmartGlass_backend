from rest_framework import serializers
from home.models import account


class passwordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = account
        fields = ['user_id', 'user_pw']
 

class userchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = '__all__'#'[__all__]' 아님 
