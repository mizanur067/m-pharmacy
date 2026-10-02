from rest_framework import serializers
from .models import NewsArticle


class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = ("id", "title", "slug", "summary", "body", "published_at", "created_at")
        read_only_fields = ("id", "author", "created_at")
