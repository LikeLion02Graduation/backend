from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # username : 아이디
    # password
    nickname=models.CharField(max_length=20)
    profile=models.TextField(null=True, blank=True)
    def __str__(self):
        return self.username