

from django.contrib import admin
from django.urls import path , include
from rest_framework import routers
router = routers.DefaultRouter()
from .views import UserViewSet, signin , signout

router.register(r'',UserViewSet, basename='user')
urlpatterns = [
 path('login/', signin, name='signin'),   
 path('logout/<int:id>/', signout, name='signout'),
 path('', include(router.urls)),  
]

