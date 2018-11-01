from django.db import models
from django.contrib.auth.models import User

class ButtonSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    button = models.CharField(max_length=50, blank=False)
    song = models.FileField(upload_to="songs/", blank=True)
