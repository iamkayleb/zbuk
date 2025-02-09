from django.db import models

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
# Create your models here.

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None