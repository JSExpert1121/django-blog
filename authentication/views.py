from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated


from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    RefreshSerializer,
    UserSerializer
)


class RegisterUserView(APIView):

    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer

    @csrf_exempt
    def post(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    serializer_class = LoginSerializer

    @csrf_exempt
    def post(self, request):

        user_serializer = self.serializer_class(data=request.data)
        user_serializer.is_valid(raise_exception=True)

        return Response(data=user_serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response({
            "logout": 'OK'
        }, status.HTTP_200_OK)


class RefreshTokenView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = RefreshSerializer

    def post(self, request):

        serializer_instance = self.serializer_class(data=request.data)
        serializer_instance.is_valid(raise_exception=True)

        return Response(serializer_instance.data, status=status.HTTP_200_OK)
