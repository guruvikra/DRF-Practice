from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
class RegularUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("The username field must be set")
        user = self.model(username=username)
        if password:
            user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        raise ValueError("RegularUser cannot have superuser privileges.")
