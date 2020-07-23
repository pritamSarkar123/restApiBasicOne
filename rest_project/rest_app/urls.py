from django.urls import path
from . import views
 
app_name='rest_app'
urlpatterns=[
    path('',views.get_all,name='get_all'),
    path('<int:eid>/',views.get_detail,name='get_detail'),
    path('auth/',views.get_auth,name='get_auth'),
]