from rest_framework import permissions, viewsets
from .models import NewsArticle
from .serializers import NewsArticleSerializer


class NewsArticleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NewsArticleSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = NewsArticle.objects.filter(is_active=True, published_at__isnull=False)
