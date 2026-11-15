from django.shortcuts import render
from django.contrib.auth.hashers import check_password,make_password
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from .models import User,Staff


@api_view(['GET'])
def my_api_view(request):
    return Response({'message': 'Hello, World!'})

@api_view(['POST'])
def create_user(request):
    try:
        name = request.data.get('name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        password = make_password(request.data.get('password'))
        try:
            user = User.objects.create(name=name, email=email, phone=phone, password=password)
            return Response({'message': 'User created successfully', 'user_id': user.id}, status=201)
        except Exception as e:
            return Response({'error': f'Error creating user: {e}'}, status=400)
    except KeyError as e:
        return Response({'error': f'Missing field: {e}'}, status=400)


@api_view(['POST'])

def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(email=email)

    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid email '},
            status=status.HTTP_401_UNAUTHORIZED
        )

    now = timezone.now()

    # 1. Check whether account is locked
    if user.locked_until and user.locked_until > now:
        remaining = user.locked_until - now

        hours = int(remaining.total_seconds() // 3600)
        minutes = int((remaining.total_seconds() % 3600) // 60)

        return Response({
            'error': f'Account locked. Try again after {hours} hours and {minutes} minutes.'
        }, status=status.HTTP_403_FORBIDDEN)

    # 2. Reset expired lock
    if user.locked_until and user.locked_until <= now:
        user.failed_login_attempts = 0
        user.locked_until = None
        user.save(update_fields=[
            'failed_login_attempts',
            'locked_until'
        ])

    # 3. Check password
    if  not check_password(password, user.password):

        user.failed_login_attempts += 1

        # 4. Lock after 3 failed attempts
        if user.failed_login_attempts >= 3:

            user.locked_until = now + timedelta(hours=24)

            user.save(update_fields=[
                'failed_login_attempts',
                'locked_until'
            ])

            return Response({
                'error': 'Too many failed attempts. Account locked for 24 hours.'
            }, status=status.HTTP_403_FORBIDDEN)

        user.save(update_fields=['failed_login_attempts'])

        remaining = 3 - user.failed_login_attempts

        return Response({
            'error': f'Invalid  password ,attempts_remaining : {remaining}',
            'attempts_remaining': remaining
        }, status=status.HTTP_401_UNAUTHORIZED)

    # 5. Successful login: reset attempts
    user.failed_login_attempts = 0
    user.locked_until = None

    user.save(update_fields=[
        'failed_login_attempts',
        'locked_until'
    ])

    return Response({
        'message': 'Login successful',
        'user_id': user.id
    }, status=status.HTTP_200_OK)



@api_view(['POST'])
def create_staff(request):
    try:
        name = request.data.get('name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        password = make_password(request.data.get('password'))
        address = request.data.get('address')
        try:
            staff = Staff.objects.create(name=name, email=email, phone=phone, password=password, address=address)
            return Response({'message': 'Staff created successfully', 'staff_id': staff.id}, status=201)
        except Exception as e:
            return Response({'error': f'Error creating staff: {e}'}, status=400)
    except KeyError as e:
        return Response({'error': f'Missing field: {e}'}, status=400)






@api_view(['POST'])
def login_staff(request):

    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        staff = Staff.objects.get(email=email)

    except Staff.DoesNotExist:
        return Response(
            {'error': 'Invalid email '},
            status=status.HTTP_401_UNAUTHORIZED
        )

    now = timezone.now()

    # Check account lock
    if staff.locked_until and staff.locked_until > now:

        remaining = staff.locked_until - now

        hours = int(remaining.total_seconds() // 3600)
        minutes = int((remaining.total_seconds() % 3600) // 60)

        return Response({
            'error': f'Account locked. Try again after {hours} hours and {minutes} minutes.'
        }, status=status.HTTP_403_FORBIDDEN)

    # Reset expired lock
    if staff.locked_until and staff.locked_until <= now:

        staff.failed_login_attempts = 0
        staff.locked_until = None

        staff.save(update_fields=[
            'failed_login_attempts',
            'locked_until'
        ])

    # Verify password
    if not check_password(password, staff.password):

        staff.failed_login_attempts += 1

        # Lock account after 3 failed attempts
        if staff.failed_login_attempts >= 3:

            staff.locked_until = now + timedelta(hours=24)

            staff.save(update_fields=[
                'failed_login_attempts',
                'locked_until'
            ])

            return Response({
                'error': 'Too many failed attempts. Account locked for 24 hours.'
            }, status=status.HTTP_403_FORBIDDEN)

        staff.save(update_fields=['failed_login_attempts'])

        return Response({
            'error': f'Invalid  password ,attempts_remaining : {3 - staff.failed_login_attempts}',
            'attempts_remaining': 3 - staff.failed_login_attempts
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Successful login
    staff.failed_login_attempts = 0
    staff.locked_until = None

    staff.save(update_fields=[
        'failed_login_attempts',
        'locked_until'
    ])

    return Response({
        'message': 'Login successful',
        'staff_id': staff.id
    }, status=status.HTTP_200_OK)