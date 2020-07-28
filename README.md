libraries used here:- Django rest feamework and request library
database<-rest api->op
to manipulate,create,delete... data we use request lib and directly update our database
here we use my sql lite as database

-------------------------------------->

functions:-
delete, create, modify, get
REST:-Representational state transfer
(get,post,put,delete) 
(get data,create data,edit data,delete data)

----------------------------------------
in your virtual env:-
pip install djangorestframework

start a project here :- "rest_project"

python manage.py runserver

----------------------------------------
python manage.py makemigrations
//

python manage.py migrate
//

---------------------------------------

python manage.py startapp rest_app

rest_project->settings->INSTALLED_APPS = [
    'rest_app',...] //regestering with main project

rest_project->rest_app->models.py->
    class Users(models.Model)://User name of table
        employee_id=models.CharField(max_length=10,unique=True)//mandatory
        name=models.CharField(max_length=100)//mandatory
        age=models.IntegerField(default=18)//mandatory
        ranking=models.FloatField()

        def upload_photo(self,filename)://filename provided by django
            path='rest_app/photo/{}'.format(filename)
            return path
        photo=models.ImageField(upload_to=upload_photo,null=True,blank=True)//optional

        def upload_file(self,filename)://filename provided by django
            path='rest_app/file/{}'.format(filename)
            return path
        resume=models.FileField(upload_to=upload_file,null=True,blank=True)//optional

        def __str__(self):
            return f"{self.employee_id}-{self.name}"

-------------------------------------------------------

rest_project->settings->
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


rest_project->urls.py
    from django.conf.urls.static import static
    from django.conf import settings
    urlpatterns=[]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

--------------------------------------------------------

python manage.py makemigrations rest_app
//makes a migration file, deals with schema of the table
//model <--rest_app\migrations\0001_initial.py--> database

python manage.py migrate rest_app
//implement the schema and make change in db

rest_project->rest_app->admin.py->
    from .models import Users
    admin.site.register(Users)//registering with admin

python manage.py createsuperuser
//

-------------------------------------------------

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'rest_project/static'),//must be present
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

python manage.py collect static
//collectiong static files(not related to DB) and put them in rest_project(basedir)/static

----------------------------------------

rest_project->settings.py->INSTALLED_APPA=[
    'rest_framework',...
]

//general convension
rest_project->rest_app->"serializers.py"
from rest_framework import serializers
from .models import Users
class "UsersSerializer"(serializers.ModelSerializer):
    #name=serializers.CharField(required=False) <-to make non required fields
    class Meta:
        model=Users
        fields='__all__' #or ('name','employee_id')
        //the fields we want to display

//
rest_project->rest_app->"api.py"
from rest_framework import.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
class UserList(APIView):
    //view functions:- get, put ,post and delete
    def get(self,request): //get <-get inbuilt
        #all employees
        objects=Users.objects.all()
        serializer=UserSerializer(objects,many=True) //as multiple items
        return Response(serializer.data)

----------------------------------------------------------

//
rest_project->rest_app->"urls.py"

from django.urls import path
from . import views 
app_name='rest_app'
urlpatterns=[
    path('',views.get_all,name='get_all'),
]

//
rest_project->rest_app->views.py

def get_all(request):
    return UserList.as_view()(request) ///(request) <-must
    //as_view <- inbuilt

//
rest_project->urls.py

from django.urls import include
urlpatterns=[
    path('rest_app/user_lists',include('rest_app.urls')),
]

------------------------------------------------
rest_project->rest_app->"api.py"

class UserList(APIView):
    def get(self,request):
        ...
    def post(self,request):
        serializer=UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) #if error occors

------------------------------------------------------------
rest_project->rest_app->"urls.py"

urlpatterns=[
    path('<int:id>/',views.get_detail,name='get_detail'),
]

rest_project->rest_app->views.py

def get_detail(request,id):
    return UserDetail.as_view()(request,id)

rest_project->rest_app->"api.py"

class UserList(APIView):
    ....
class UserDetail(APIView):
    def get(self,request,eid):
        try:
            modelObjects=Users.objects.get(id=eid)
        except Users.DoesNotExist:
            return Response(f'Employee with general ID {eid} not found in DB',status=status.HTTP_404_NOT_FOUND)
        serializer=UsersSerializer(modelObjects)
        return Response(serializer.data)
    def put(self,request,e_id):
        try:
            modelObjects=Users.objects.get(id=eid)
        except Users.DoesNotExist:
            return Response(f'Employee with general ID {eid} not found in DB',status=status.HTTP_404_NOT_FOUND)
        serializer=UsersSerializer(modelObjects,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) #if error occors

***************** we have to provide all provperty values in case of put request**** other wise reduired fildes generates bad request .... to avoid this

<1> in serializer level
    class UserSerializer(....):
        fieldName=serializers.CharField(required=False)
        ....
        class Meta:
            ...

//  
    class UsersSerializer(serializers.ModelSerializer):
        name=serializers.CharField(required=False)
        employee_id=serializers.CharField(required=False)
        age=serializers.IntegerField(required=False)
        class Meta:
            ....

<2> in Model level
    class User(...):
        fieldName=models.CharField(...,null=True,blank=True)

    
***************************
-----------------------------------------------------

//deletion
rest_project->rest_app->"api.py"

class UserDetail(APIView):
    def get_user(self,eid):
        try:
            modelObjects=Users.objects.get(id=eid)
            return modelObjects
        except Users.DoesNotExist:
            return None
    def get(self,request,eid):
        if not self.get_user(eid):
            return Response(f'Employee with general ID {eid} not found in DB',status=status.HTTP_404_NOT_FOUND)
        serializer=UsersSerializer(self.get_user(eid))
        return Response(serializer.data)
    def put(self,request,eid):
        if not self.get_user(eid):
            return Response(f'Employee with general ID {eid} not found in DB',status=status.HTTP_404_NOT_FOUND)
        serializer=UsersSerializer(self.get_user(eid),data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) #if error occors
    def delete(self,request,eid):
        if not self.get_user(eid):
            return Response(f'Employee with general ID {eid} not found in DB',status=status.HTTP_404_NOT_FOUND)
        modelObj=self.get_user(eid)
        modelObj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

--------------------------------------------------------------------------------

authintication 

rest_project->settings.py->
INSTALLED_APPA=[
    'rest_framework',
    'rest_framework.authtoken',...
]
...
REST_FRAMEWORK={
    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.IsAuthenticated', <-checks whether user has enough permissions
    ],
    'DEFAULT_AUTHENTICATION_CLASSES':( <-by which authenticatiom method u access data 
        'rest_framework.authentication.BasicAuthentication',<- username password based
        'rest_framework.authentication.SessionAuthentication',<- if user authenticated in any other tab of the same site , then they can use same rest api-><-if logged in one tab, rest api access in another tab->
        'rest_framework.authentication.TokenAuthentication',<-- vvi for python req lib
    )
}

//
python manage.py makemigrations           ---------auth token requires a table for authentication

//
python manage.py migrate             ---------auth token requires a table for authentication

-----------------------------------------------------
rest_project->rest_app->"api.py"

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token //Token is an authtoken table
...
class UserAuthentication(ObtainAuthToken):
    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True) #if not valid raise exception
        user=serializer.validated_data['user']
        token,created=Token.objects.get_or_create(user=user)
        #OR token=Token.objects.get_or_create(user=user)[0]
        return Response(token.key)
#{username,password}->(post method...)->token to the corresponding user##

rest_project->urls.py

    path('rest_app/user_list/',include('rest_app.urls')),

rest_project->rest_app->"urls.py"

    path('auth/',views.get_auth,name='get_auth'),

rest_project->rest_app->views.py

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

