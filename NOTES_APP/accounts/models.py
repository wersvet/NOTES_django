# accounts/models.py

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    totp_secret = models.CharField(max_length=32, blank=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"
