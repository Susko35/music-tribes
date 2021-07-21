from django.db import models
from Tribe.models import tribe
from django.utils import timezone

# Create your models here.

class playlist(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    tribe = models.ForeignKey(tribe,on_delete=models.CASCADE,)
    time_created= models.DateTimeField(default=timezone.now )

    def __str__(self):
            return self.name