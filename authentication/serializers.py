from rest_framework.serializers import ModelSerializer, EmailField, CharField, ValidationError
from django.contrib.auth import authenticate

from .models import User


# class LoginSerializer(ModelSerializer):
#     email = EmailField()
#     password = CharField(write_only=True)

#     def validate(self, data):
#         user = authenticate(**data)
#         if user is None:
#             raise ValidationError("Invalid credentials")
#         return {"user": user}


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role']
