from django.contrib import admin
from .models import News, Post, Comment, Category

admin.site.register(News)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
