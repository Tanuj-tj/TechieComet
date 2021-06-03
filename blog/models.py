from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=20,default="")
    title = models.CharField(max_length=100)
    heading = models.CharField(max_length=100)
    content = models.TextField()
    slug = models.CharField(max_length=130)
    timeStamp = models.DateField(blank=True)
    thumbnail = models.ImageField(upload_to='blog/images',default="")

    def __str__(self):
        return f"{self.title} - {self.author}"


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,null=True)
    timestamp = models.DateTimeField(default=now)