from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return f"User: id-{self.pk} username:{self.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile/', null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Profile: id-{self.pk} username:{self.user.username}"
