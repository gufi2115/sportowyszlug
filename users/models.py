from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone


class ProfileM(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    short_intro = models.CharField(max_length=150, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True,upload_to='profiles/', default='profiles/papierosek.png')
    verification_code = models.CharField(max_length=6, blank=False, null=False)
    verification_code_from_user = models.CharField(max_length=6, blank=True, null=True)
    created = models.DateTimeField(default=datetime.now(timezone.utc), blank=True)


    def __str__(self):
        return str(self.user.username)