from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import EmailUserManager


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, db_index=True, blank=True)
    full_name = models.CharField(max_length=128, blank=True, null=True)
    first_name = None
    last_name = None
    username = None

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:
        # permissions = []
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    objects = EmailUserManager()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.full_name or self.email

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('users', kwargs={'pk': self.pk})

