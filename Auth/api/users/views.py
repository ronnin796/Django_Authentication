from django.shortcuts import render
import random
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated , AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, get_user_model , logout
from rest_framework.permissions import IsAuthenticated, AllowAny
import re
# Create your views here.
def generate_session_token(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range (97,123)]+[str(i) for i in range (10)]) for _ in range (length))
@csrf_exempt
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'error': 'Send a post request with valid parameters'})
    
    username = request.POST['email']
    password = request.POST['password']

    if not  re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", username):
        return JsonResponse({'error': 'Invalid email format'})
    
    if len(password) < 8:
        return JsonResponse({'error': 'Password must be at least 8 characters long'})
    
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(email = username)
        if user.check_password(password):
            usr_dict = UserModel.objects.filter(email=username).values().first()
            usr_dict.pop('password')

            if user.session_token != "0":
                user.session_token = "0"
                user.save()
                return JsonResponse({'error': 'User already logged in'})
            
            token  = generate_session_token()
            user.session_token = token
            user.save()
            login(request, user)
            return JsonResponse({'token': token, 'user': usr_dict})
        else:
            return JsonResponse({'error': 'Invalid Password '})
    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'})
    
def signout (request , id):
    logout(request)
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = "0"
        user.save()

    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'})
    return JsonResponse({'message': 'User logged out successfully'})

class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = { 'create' : [AllowAny]}
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
