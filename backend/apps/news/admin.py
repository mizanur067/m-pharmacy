from django.contrib import admin
from .models import NewsArticle


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "is_active")
    prepopulated_fields = {"slug": ("title",)}
