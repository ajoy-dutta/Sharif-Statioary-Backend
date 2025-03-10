# Authentication/authentication_backend.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)  # Username is email in this case
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

