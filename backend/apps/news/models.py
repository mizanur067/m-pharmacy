from django.conf import settings
from django.db import models
from apps.core.models import BaseModel


class NewsArticle(BaseModel):
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True)
    summary = models.CharField(max_length=400)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="news_articles")
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-published_at", "-created_at")

