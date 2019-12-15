from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer

# Create your views here.


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get(self, request):

        user_serializer = self.serializer_class(request.user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def put(self, request):

        user = request.data.get('user', {})

        # for (key, value) in user.items():
        #     setattr(instance, key, value)

        user_serializer = self.serializer_class(
            request.user, data=user, partial=True)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)
