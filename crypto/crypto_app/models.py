from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=355)
    publisher = models.CharField(max_length=300)
    description = models.TextField()
    blog = models.TextField()
    photo = models.ImageField(upload_to='blog_photo')
    pub_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class History(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add = True)
    task = models.CharField(max_length=300)