from rest_framework import serializers
from home.models import Account


class passwordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'user_pw']
 

class userchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'#'[__all__]' 아님

