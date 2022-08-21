
from ast import Return
import json
from msilib.schema import Class
from re import template
from telnetlib import STATUS
from home.models import Company, Account

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def Sign_up(request) :
    
    response_data ={
        "code": 200,
        "message": "회원가입에 성공하였습니다."
        }
    
     #데이터중 company_name 찾기
    if request.method=="POST":
        #json , 받아오는 방법 loads
        received_json_data = json.loads(request.body.decode("utf-8"))
      #받아온 json을 확인 할 수 있음   print(received_json_data)
      #대소문자를 가리지 않고 comapany_name을 받아올 것이기 때문에 iexact
        Be_company = Company.objects.filter(company_name__iexact=received_json_data["company_name"]).values('company_name')
        Be_user_id = Account.objects.filter(user_id__iexact=received_json_data["user_id"]).values("user_id")
        print( Be_company)
        print(received_json_data["company_name"])
        #filter만 했을때 <QuerySet [<Company: Company object (1)>]>
        #values까지 했을때 <QuerySet [{'company_name': '한이음'}]>
        
        
        #company name이 동일 한 것이 없을 때 
        if Be_company.first()==None :
            Company.objects.create(company_name=received_json_data["company_name"])
            company_id_Query =Company.objects.filter(company_name__iexact=received_json_data["company_name"]).prefetch_related('company').values('company_id')
            a=company_id_Query.first().get('company_id')
            #<QuerySet [{'company_id': 1}]>
            #Company object (1) instance
            company_id_instance= Company.objects.filter(company_id=a)
            company_id_instance=company_id_instance.first()
            received_json_data.pop('company_name')
            Account.objects.create(company_id=company_id_instance,**received_json_data)
            print("company_name 생성 후 회원가입 완료 ")
            return JsonResponse(response_data, status=200)
            #id 조회해서 가져오기 
        #company name이 동일 한 것이 있을 때 
        else : 
            if Be_user_id.first()==None :
                print("원래 company_name조회하여 company_id 가져옴")
                company_id_Query =Company.objects.filter(company_name__iexact=received_json_data["company_name"]).prefetch_related('company').values('company_id')
                a=company_id_Query.first().get('company_id')
                company_id_instance= Company.objects.filter(company_id=a)
                company_id_instance=company_id_instance.first()
                received_json_data.pop('company_name')
                Account.objects.create(company_id=company_id_instance,**received_json_data)
                print("회원가입 완료 ")
                return JsonResponse(response_data, status=200)
            else :
              return JsonResponse({'message' : 'user_id가 중복되었습니다.'}, status=400)
         
    elif request.method=="GET":
        data= Account.objects.all() 
        return JsonResponse({'message':'get'}, status=200)
    
@csrf_exempt
def login(request) :
    response_data ={
        "code": 200,
        "message": "로그인에 성공하였습니다."
        }
    
     #데이터중 company_name 찾기
    if request.method=="POST":
        #json , 받아오는 방법 loads
        received_json_data = json.loads(request.body.decode("utf-8"))
        user_id=Account.objects.filter(user_id__iexact=received_json_data["user_id"]).values("user_id")
        user_pw=Account.objects.filter(user_pw__iexact=received_json_data["user_pw"]).values("user_pw")
        
        if user_id.first()==None :
             return JsonResponse({'message':'user_id가 존재하지 않습니다.'}, status=200)
        else :
            if user_pw.first()==None:
                return JsonResponse({'message':'비밀번호가 틀리셨습니다.'}, status=200)   
            else :
                return JsonResponse(response_data, status=200)
            
    elif request.method=="GET":
        return JsonResponse({'message':'login api입니다.'}, status=200)
    
@csrf_exempt
def logout(request,user_id) :
    if request.method=="GET":
        user_id=Account.objects.filter(user_id__iexact=user_id).values("user_id")
        if user_id.first()==None :
            return JsonResponse({'message':'user_id를 다시 입력해주세요.'}, status=200)
        else :
            return JsonResponse({'message':'로그아웃 되었습니다.'}, status=200)
