from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.response import Response

from .models import News, Post, Comment
from django.contrib.auth.models import User
from rest_framework.status import HTTP_400_BAD_REQUEST


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    post_id = serializers.SerializerMethodField()

    def get_author(self, obj):
        return {'id': obj.author.id, 'username': obj.author.username}

    def get_post_id(self, obj):
        return obj.post.id

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'author', 'post_id']
        depth = 1
        # required = False


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, required=False)
    comment_count = serializers.SerializerMethodField()
    categories = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', required=False)

    def get_author(self, obj):
        return {'id': obj.author.id, 'username': obj.author.username}

    def get_comment_count(self, obj):
        return obj.comments.count()

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({'error': 'The slug must be unique.'}, status=HTTP_400_BAD_REQUEST)

    class Meta:
        model = Post
        fields = ['comment_count', 'id', 'title', 'slug', 'content', 'created_at', 'updated_at', 'categories', 'author',
                  'comments']
