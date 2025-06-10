"""
Authentication views for user management.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationView(APIView):
    """
    User registration endpoint.
    """
    
    def post(self, request):
        """
        Register a new user.
        
        Expected payload:
        {
            "username": "string",
            "email": "string", 
            "password": "string"
        }
        """
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            
            # Validate required fields
            if not username or not email or not password:
                return Response(
                    {'error': 'Username, email, and password are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return Response(
                    {'error': 'Username already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if User.objects.filter(email=email).exists():
                return Response(
                    {'error': 'Email already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            return Response(
                {
                    'message': 'User created successfully',
                    'user_id': user.id,
                    'username': user.username
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {'error': f'Registration failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )