from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notes(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    note = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.note[:10]
    
class DarkMode(models.Model):
    active = models.BooleanField(default=False)
