from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    subscription_type = models.CharField(max_length=20, choices=[
        ('free', 'Free'),
        ('premium', 'Premium')
    ], default='free')
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.email
