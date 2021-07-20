from django.db import models
from django.contrib.auth.models import User


class profile_info(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture=models.ImageField(null=True, blank=True, upload_to="ProfilePictures/")
    def __str__(self):
        return self.user.username