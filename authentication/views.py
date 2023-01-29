from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

from .models import User
from .serializers import UserDetailSerializer, UserListSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class UserViewSet(ModelViewSet):

    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer

    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["is_staff"] = True
        data["password"] = make_password(request.data["password"])
        serializer = UserDetailSerializer(data=data)

        list_serializer = UserListSerializer(data=data)
        list_serializer.is_valid(raise_exception=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(data=list_serializer.data)

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'update':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()

