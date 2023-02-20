from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin

class User(AbstractUser):

    Management = 'Management'
    Sales = 'Sales'
    Support = 'Support'

    ROLE_CHOICES = (
        (Management, 'Management'),
        (Sales, 'Sales'),
        (Support, 'Support'),
    )

    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(null=False, unique=True)
    role = models.CharField(max_length=25, choices=ROLE_CHOICES, null=False)
    password = models.CharField(max_length=1000, null=False)

    def __str__(self):
        return self.username