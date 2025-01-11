from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

from .serializers import RegisterSerializer, UserSerializer, TokenSerializer


class RegisterUserApi(APIView):
    """
    API view for user registration
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserSerializer(user)

            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)

            # Prep response data to include JWT token
            response_data = user_serializer.data
            response_data['token'] = token

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainTokenApi(APIView):
    """
    API view to generate JWT token for authentication
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # NOTE: JWT tokens are stateless; reusing them requires that they be stored
            # For simplicity, we'll always issue a new token
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)

            return Response({'token': token}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
