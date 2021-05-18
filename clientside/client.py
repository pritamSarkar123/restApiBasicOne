# any user who is registered , can CRUD on databases
import requests
from random import random
from random import randint
from random import shuffle
ALPHA=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
URL='http://127.0.0.1:8000/'
#get auth token post
def get_token(delete):
    url=f'{URL}rest_app/user_list/auth/'
    data=None
    if delete:
    	data={'username':'deleter','password':'pritams12345@'}
    else:
    	data={'username':'creator','password':'pritams12345@'}
    t=requests.post(url,data=data).json()
    print(t)
    return t

def get_data(): #get data get
    url=f'{URL}rest_app/user_list/'
    header={'Authorization':f'Token {get_token(False)}'}
    response=requests.get(url,headers=header)
    user_data=response.json()
    for u in user_data:
        print(u)

def create_new(count): #post data
    url=f'{URL}rest_app/user_list/'
    header={'Authorization':f'Token {get_token(False)}'}
    shuffle(ALPHA)
    fname=''.join(ALPHA[:6])
    lname=''.join(ALPHA[-6:])
    data={
            "name": "{} {}".format(fname,lname),"employee_id": '100{}'.format(count),"age": randint(20,31),"ranking": round(random()*100,3)
        }
    response=requests.post(url,data=data,headers=header)
    print(response.text,response.status_code)


def edit(eid,name=None,employee_id=None,age=None,ranking=None): #put data
    url=f'{URL}rest_app/user_list/{eid}/' #### last '/' is vvi
    header={'Authorization':f'Token {get_token(False)}'}
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
    header={'Authorization':f'Token {get_token(True)}'}
    response=requests.delete(url,headers=header)
    print(f" after deletion {response.status_code}")

for i in range(30):
    create_new(i)

# for i in range(53,83):
#     delete(i)

