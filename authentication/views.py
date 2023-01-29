from django.contrib.auth import login, logout
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# class LoginView(views.APIView):

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]
#         login(request, user)
#         return Response(UserSerializer(user).data)

# class LogoutView(views.APIView):

#     def post(self, request):
#         logout(request)
#         return Response(status=status.HTTP_204_NO_CONTENT)



class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer
    detail_serializer_class = UserSerializer

    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["is_staff"] = True
        serializer = UserSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'update':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()

