from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserProfileUpdateSerializer, UserRegistrationSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Send verification email
        send_verification_email(user)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_verification_email(user):
    """Send email verification to the user"""
    try:
        profile = user.userprofile
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{profile.verification_token}/"
        send_mail(
            'Verify your email address',
            f'Hello {user.username},\n\nPlease verify your email address by clicking the link below:\n\n{verification_url}\n\nThank you for joining VirtualCoworking!',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except UserProfile.DoesNotExist:
        pass  # User profile not created yet


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response(UserSerializer(user).data)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Successfully logged out'})


@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    serializer = UserProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        # Also update user fields if provided
        user = request.user
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.save()
        
        # Return full profile
        full_profile = UserProfileSerializer(profile)
        return Response(full_profile.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request, token):
    """Verify user's email address"""
    profile = get_object_or_404(UserProfile, verification_token=token)
    profile.is_verified = True
    profile.save()
    return Response({'message': 'Email verified successfully'})


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        # In a real application, you would generate a token and send a reset link
        # For this example, we'll just send a simple email
        send_mail(
            'Password Reset Request',
            f'Hello {user.username},\n\nYou have requested to reset your password. '
            'In a real application, you would receive a link to reset your password.\n\n'
            'For now, please contact support to reset your password.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response({'message': 'Password reset email sent'})
    except User.DoesNotExist:
        # For security reasons, we don't reveal if the email exists
        return Response({'message': 'Password reset email sent'})