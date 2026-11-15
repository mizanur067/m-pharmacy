from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User


@api_view(['GET'])
def my_api_view(request):
    return Response({'message': 'Hello, World!'})

@api_view(['POST'])
def create_user(request):
    try:
        name = request.data.get('name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        password = request.data.get('password')
        try:
            user = User.objects.create(name=name, email=email, phone=phone, password=password)
            return Response({'message': 'User created successfully', 'user_id': user.id}, status=201)
        except Exception as e:
            return Response({'error': f'Error creating user: {e}'}, status=400)
    except KeyError as e:
        return Response({'error': f'Missing field: {e}'}, status=400)


@api_view(['POST'])
def login_user(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email, password=password)
            return Response({'message': 'Login successful', 'user_id': user.id}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=401)
    except KeyError as e:
        return Response({'error': f'Missing field: {e}'}, status=400)

