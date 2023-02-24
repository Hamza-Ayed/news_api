
from django.db import models

class News(models.Model):
    objects = None
    title = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True,null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.URLField(blank=True, null=True,unique=False)
    link = models.URLField(blank=True, null=True,unique=True)


    def __str__(self):
        return self.title
