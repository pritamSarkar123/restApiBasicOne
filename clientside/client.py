import requests
from random import random
from random import randint
from random import shuffle
ALPHA=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
URL='http://127.0.0.1:8000/'
#get auth token post
def get_token():
    url=f'{URL}rest_app/user_list/auth/'
    return requests.post(url,data={'username':'pritam','password':'pritams1'}).json()

def get_data(): #get data get
    url=f'{URL}rest_app/user_list/'
    header={'Authorization':f'Token {get_token()}'}
    response=requests.get(url,headers=header)
    user_data=response.json()
    for u in user_data:
        print(u)

def create_new(count): #post data
    url=f'{URL}rest_app/user_list/'
    header={'Authorization':f'Token {get_token()}'}
    shuffle(ALPHA)
    fname=''.join(ALPHA[:6])
    lname=''.join(ALPHA[-6:])
    data={
            "name": "{} {}".format(fname,lname),"employee_id": '100{}'.format(count),"age": randint(20,31),"ranking": round(random()*100,3)
        }
    response=requests.post(url,data=data,headers=header)
    print(response.text,response.status_code)
# for i in range(30):
#     create_new(i)

def edit(eid,name=None,employee_id=None,age=None,ranking=None): #put data
    url=f'{URL}rest_app/user_list/{eid}/' #### last '/' is vvi
    header={'Authorization':f'Token {get_token()}'}
    data={}
    if name:
        data["name"]=name
    if employee_id:
        data["employee_id"]=employee_id
    if age:
        data["age"]=age
    if ranking:
        data["ranking"]=ranking
    response=requests.put(url,data=data,headers=header)
    print(response.text,response.status_code)

# edit(7,name="Eshani Jas",ranking=1.0)
def delete(eid): #delete data
    url=f'{URL}rest_app/user_list/{eid}/' #### last '/' is vvi
    header={'Authorization':f'Token {get_token()}'}
    response=requests.delete(url,headers=header)
    print(response.status_code)
for i in range(30):
    if i>7:
        delete(i)
