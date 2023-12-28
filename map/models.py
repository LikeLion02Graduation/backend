from django.db import models
from accounts.models import *
from django.utils.timezone import now

class TimeStamp(models.Model):
    created_at = models.DateTimeField(default=now)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Hashtag(models.Model):
    tagname = models.CharField(max_length=100)
    enable = models.BooleanField(default=False)
    def __str__(self):
        return self.tagname

class Map(TimeStamp):
    user = models.ForeignKey(User, related_name='map_user',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=20)
    hashtag = models.ManyToManyField(Hashtag,related_name='map_hashtag',blank=True)
    img =  models.TextField()
    description = models.TextField()
    buyers = models.ManyToManyField(User,related_name='buyers',blank=True)
    def __str__(self):
        return str(self.id)+" "+self.name+" - "+self.user.nickname

class Place(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    link = models.TextField()
    def __str__(self):
        return self.name

class Recommend(TimeStamp):
    user = models.ForeignKey(User, related_name='recom_user',on_delete=models.CASCADE)
    place = models.ManyToManyField(Place,related_name='recom_place')
    title = models.CharField(max_length=100)
    content = models.TextField()
    hashtag = models.ManyToManyField(Hashtag,related_name='recom_hashtag',blank=True)
    map = models.ForeignKey(Map, related_name='recom_map',on_delete=models.CASCADE)

class React(TimeStamp):
    EMOJIS = ((1, 1), (2, 2), (3, 3), (4, 4))
    user = models.ForeignKey(User, related_name='react_user',on_delete=models.CASCADE)
    recommend = models.ForeignKey(Recommend,related_name='react_recom',on_delete=models.CASCADE)
    emoji = models.IntegerField(choices=EMOJIS)
    content = models.TextField()

class Alert(TimeStamp):
    user = models.ForeignKey(User, related_name='alert_user',on_delete=models.CASCADE)
    recommend = models.ForeignKey(Recommend,related_name='alert_recom',on_delete=models.CASCADE)
