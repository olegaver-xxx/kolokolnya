from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class EmailUserManager(BaseUserManager):

    def create_user(self, email, password=None, is_staff=False, is_superuser=False, is_active=False):
        user = self.model(email=self.normalize_email(email),
                          is_staff=is_staff,
                          is_active=is_active,
                          is_superuser=is_superuser,
                          date_joined=timezone.now())
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        return self.create_user(email, password, is_staff=True, is_superuser=True, is_active=True)
