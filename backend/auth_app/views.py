from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer, UserSerializer


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
