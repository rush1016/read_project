from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to get a user by email first
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # If a user with the email is not found, try to get a user by username
            user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            return user
        return None