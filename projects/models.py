from datetime import timezone
from tkinter.constants import CASCADE

from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.db import models
from embed_video.fields import EmbedVideoField
import uuid


class ProjectsM(models.Model):
    title = models.CharField(max_length=255, blank=True, null=False)
    date = models.DateTimeField(auto_now_add=True)
    video = EmbedVideoField()
    age = models.CharField(max_length=3, blank=True, null=True)
    time = models.CharField(max_length=15, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-date']



class ReviewM(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    project = models.ForeignKey(ProjectsM, on_delete=models.CASCADE, related_name="review")
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=255, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.value


class RanksM(models.Model):
    rank = models.CharField(max_length=25, null=True, blank=True, default='Unranked')
    rank_image = models.ImageField(null=True, blank=True, default='/unranked.png')

    def __str__(self):
        return self.rank
