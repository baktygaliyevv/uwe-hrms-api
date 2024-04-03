from django.contrib.auth.backends import ModelBackend

class CustomUserModelBackend(ModelBackend):
    def user_can_authenticate(self, user):
        return True
