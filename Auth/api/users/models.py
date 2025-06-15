from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255,  null=True , default='Annonymous')
    email = models.EmailField(unique=True, max_length=255, null=True)

    username = None  # Disable username field
    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []  # No required fields other than email
    phone = models.CharField(max_length=15, null=True, blank=True)

    gender = models.CharField(
        max_length=10,
    )
    session_token = models.CharField(max_length=10 , default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
                            