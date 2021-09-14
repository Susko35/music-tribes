from django.contrib import admin
from .models import tribe, members, message
# Register your models here.

admin.site.register(tribe)
admin.site.register(members)
admin.site.register(message)