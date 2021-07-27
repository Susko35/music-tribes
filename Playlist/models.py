from django.db import models
from Tribe.models import tribe
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class playlist(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    tribe = models.ForeignKey(tribe,on_delete=models.CASCADE,)
    time_created= models.DateTimeField(default=timezone.now )

    def __str__(self):
            return self.name


class song(models.Model):
    artist=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    url=models.CharField(max_length=120)
    duration=models.DurationField()
    number_likes=models.IntegerField(default=0)
    number_comments=models.IntegerField(default=0)
    playlist = models.ForeignKey(playlist, on_delete=models.CASCADE,)
    time_created=models.DateTimeField(default=timezone.now )
    user_added=models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
            return self.title


class like(models.Model):
    song=models.ForeignKey(song, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints=[
            models.UniqueConstraint(name='user_like', fields = ['song','user'])
        ]
    def __str__(self):
        return self.user.username


class comment(models.Model):
    song=models.ForeignKey(song,blank=True, related_name="comments", on_delete=models.CASCADE)
    user=models.ForeignKey(User,blank=True, on_delete=models.CASCADE)
    text=models.CharField(max_length=300)
    time_posted=models.DateTimeField(default=timezone.now )

    def __str__(self):
        return self.user.username