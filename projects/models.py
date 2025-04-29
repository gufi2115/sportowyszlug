from django.db import models
from embed_video.fields import EmbedVideoField
from users.models import ProfileM

class ProjectM(models.Model):
    owner = models.ForeignKey(ProfileM, on_delete=models.CASCADE, related_name="project", null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, null=False)
    date = models.DateTimeField(auto_now_add=True)
    video = EmbedVideoField()
    age = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-date']



class ReviewM(models.Model):
    VOTE_TYPE = (
        ('up', '👍'),
        ('down', '👎')
    )
    project = models.ForeignKey(ProjectM, on_delete=models.CASCADE, related_name="review")
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=255, choices=VOTE_TYPE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(ProfileM, on_delete=models.CASCADE, related_name="review_owner", null=True, blank=True)


    def __str__(self):
        return self.value


class RanksM(models.Model):
    owner = models.ForeignKey(ProfileM, on_delete=models.CASCADE, related_name="ranks", null=True, blank=True)
    rank = models.CharField(max_length=25, null=False, blank=False, default='Unranked')
    rank_image = models.ImageField(null=True, blank=True, default='unranked.png')
    created_at = models.DateTimeField(auto_now_add=True)


    # def __str__(self):
    #     return self.rank