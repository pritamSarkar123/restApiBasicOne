from django.db import models

# Create your models here.
class Users(models.Model):#User name of table
    employee_id=models.CharField(max_length=10,unique=True)#mandatory
    name=models.CharField(max_length=100)#mandatory
    age=models.IntegerField(default=18)#mandatory
    ranking=models.FloatField()

    def upload_photo(self,filename):#filename provided by django
        path='rest_app/photo/{}'.format(filename)
        return path
    photo=models.ImageField(upload_to=upload_photo,null=True,blank=True)#optional

    def upload_file(self,filename):#filename provided by django
        path='rest_app/file/{}'.format(filename)
        return path
    resume=models.FileField(upload_to=upload_file,null=True,blank=True)#optional

    def __str__(self):
        return f"{self.employee_id}-{self.name}"