from rest_framework import serializers
from sqlalchemy import values
from home.models import Account,Company
from drf_writable_nested.serializers import WritableNestedModelSerializer

class loginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'user_pw']

   
class companySerializer(serializers.ModelSerializer):
   
    class Meta:		
        model = Company		
        #fields에서 대소문자 구분함
        fields ='__all__'
        
    def create(self, validated_data):
        Company.objects.create(**validated_data)    
 
   

class signupSerializer(serializers.ModelSerializer):
    
    user_pw= serializers.CharField(
        max_length = 128,
        min_length = 4,
        write_only = True
    )

    Company_name= companySerializer()
    # 토큰 - 나중에 필요할 때 이용 : 테이블 하나 더 만들어서 저장하면 됌 , 유효기간 설정가능 
    #token = serializers.CharField(max_length=255, read_only=True)
 
    class Meta:
        model = Account
        fields = '__all__' 
        depth = 2
    
    extra_kwargs = {
        'Company_name': {'allow_null': True, 'required': False},
        'Company_id': {'allow_null': True, 'allow_blank': True, 'required': False}, 
  
    }

        


    
