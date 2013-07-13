from django.db import models

try:
    from django.contrib.auth.models import AbstractUser
except ImportError:
    from django.db.models import Model as AbstractUser


class CustomUser(AbstractUser):
    extra_field = models.CharField(max_length=2)
    new_username_field = models.CharField(unique=True, max_length=20)

    USERNAME_FIELD = 'new_username_field'