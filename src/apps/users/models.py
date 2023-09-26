from django.contrib.auth.models import AbstractUser
from django.db import models


# class MyUser(AbstractUser):
#     is_admin = models.BooleanField(default=False)


class User(AbstractUser):
    pass

