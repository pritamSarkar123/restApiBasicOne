from django.shortcuts import render
from .api import UserList
from .api import UserDetail
from .api import UserAuthentication
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_all(request):
    return UserList.as_view()(request)

@csrf_exempt
def get_detail(request,eid):
    return UserDetail.as_view()(request,eid)
    
@csrf_exempt
def get_auth(request):
    return UserAuthentication.as_view()(request)
    