from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import *

class UserAuthentication(ObtainAuthToken):
    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token,created=Token.objects.get_or_create(user=user)
        return Response(token.key)

class UserList(APIView):
    def get(self,request):
        #getting all objects
        modelObjects=Users.objects.all() #imported with in serializers
        serializer=UsersSerializer(modelObjects,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) #if error occors

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