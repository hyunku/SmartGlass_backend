from re import I
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection




#크랙 정보 목록 조회(사용자)
def show_user_crack_list(request, user_id):
    
    list=[]

    cursor = connection.cursor()
    query = f"select raw_data.raw_data_id,building.name,picture,floor,room,details\
        from glass join building on glass.target_building = building.building_id\
        join raw_data on glass.user_id = raw_data.upload_user_id\
        join issue on issue.raw_data_id = raw_data.raw_data_id\
        join account on glass.user_id = account.user_id\
        where account.user_id = '{user_id}';"
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    
    col = "raw_data_id,name,picture,floor,room,details".split(",")

    for i in data:
        list.append(dict(zip(col,i)))

    crack_list = {'crack_list' : list}

    return JsonResponse(crack_list)

#크랙 정보 목록 조회(관리자)
def show_manager_crack_list(request, user_id):
    
    list=[]

    cursor = connection.cursor()
    query = f"with company(manager_company_id) as( \
        select company_id from account where user_id = '{user_id}'\
    )\
    select raw_data.raw_data_id,building.name,picture,floor,room,details\
    from glass join building on glass.target_building = building.building_id\
    join raw_data on glass.user_id = raw_data.upload_user_id\
    join issue on issue.raw_data_id = raw_data.raw_data_id\
    join account on glass.user_id = account.user_id\
    where account.company_id in (select manager_company_id from company);"
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()

    col = "raw_data_id,name,picture,floor,room,details".split(",")

    for i in data:
        list.append(dict(zip(col,i)))

    crack_list = {'crack_list' : list}

    return JsonResponse(crack_list)

#연결할 글래스 선택
def show_glass_list(request):
    list=[]
    cursor = connection.cursor()
    query = "select glass_name from glass;"
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    print(data)
    col = ["glass_name"]
    
    for i in data:
        list.append(dict(zip(col,i)))

    glass_list = {'glass_list' : list}

    return JsonResponse(glass_list)

#연결할 건물 선택
def show_building_list(request,user_id):
    list=[]
    cursor = connection.cursor()
    query = f" with company(user_company_id) as(\
        select company_id from account where user_id = 'user'\
    )\
    select name from building\
    where building.company_id in (select user_company_id from company)"
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
   
    col = ['name']

    for i in data:
        list.append(dict(zip(col,i)))

    building_list = {'building_list' : list}

    return JsonResponse(building_list)

