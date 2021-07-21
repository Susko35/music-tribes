from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class tribe(models.Model):
    genre=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    users=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="usersRel", through='members')
    image=models.ImageField(null=True, blank=True, upload_to="TribePictures/")
    chieftain = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        blank=True,
        related_name="chief",
    )
    def __str__(self):
            return self.name
    

class members(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, )
    tribe = models.ForeignKey(tribe,on_delete=models.CASCADE,)
    def __str__(self):
        template = '{0.user.username} {0.tribe.name}'
        return template.format(self)
        
    class Meta:
        constraints=[
            models.UniqueConstraint(name='membership', fields = ['user','tribe'])
        ]


