from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User

class Topic(models.Model):
    """A class to write blog """
    title = models.CharField(max_length=200, default='Title')
    description = models.TextField(default='Description')
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if len(self.title) > 30:
            return f"{self.title[:30]}..."
        else:
            return self.title

class Post(models.Model):
    """A class to add article"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='Title')
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Posts"

    def __str__(self):
        if len(self.text) > 30:
            return f"{self.text[:30]}..."
        else:
            return self.text
