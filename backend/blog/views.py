from django.db import models
from django.db.models import Count, Q
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Tag, Article, Comment, FriendlyLink, PersonalLink, SiteSettings
from .serializers import (
    CategorySerializer, TagSerializer,
    ArticleListSerializer, ArticleDetailSerializer,
    CommentSerializer, FriendlyLinkSerializer,
    PersonalLinkSerializer, SiteSettingsSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.annotate(article_count=Count('article')).order_by('name')
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.filter(status='p').annotate(
        comment_count=Count('comment')
    ).order_by('-is_top', '-created_at')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'tags']
    search_fields = ['title', 'summary', 'content']
    ordering_fields = ['created_at', 'views']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increase_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def archives(self, request):
        from django.db.models import Count
        from django.db.models.functions import ExtractYear, ExtractMonth
        
        archives = Article.objects.filter(status='p').annotate(
            year=ExtractYear('created_at'),
            month=ExtractMonth('created_at')
        ).values('year', 'month').annotate(
            count=Count('id')
        ).order_by('-year', '-month')
        
        return Response(archives)

    @action(detail=False, methods=['get'])
    def hot(self, request):
        hot_articles = self.queryset.order_by('-views')[:5]
        serializer = ArticleListSerializer(hot_articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_articles = self.queryset.order_by('-created_at')[:5]
        serializer = ArticleListSerializer(recent_articles, many=True)
        return Response(serializer.data)


class CommentViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Comment.objects.filter(is_approved=True, parent=None).order_by('-created_at')
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['article']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FriendlyLinkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FriendlyLink.objects.filter(is_active=True).order_by('sort_order', 'id')
    serializer_class = FriendlyLinkSerializer


class PersonalLinkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PersonalLink.objects.filter(is_active=True).order_by('sort_order', 'id')
    serializer_class = PersonalLinkSerializer


@api_view(['GET'])
def site_settings(request):
    settings = SiteSettings.objects.first()
    if settings:
        serializer = SiteSettingsSerializer(settings)
        return Response(serializer.data)
    return Response({
        'site_name': '个人博客',
        'site_description': '欢迎来到我的个人博客',
        'site_keywords': '',
        'github_url': '',
        'avatar': '',
        'about_content': ''
    })


@api_view(['GET'])
def statistics(request):
    data = {
        'article_count': Article.objects.filter(status='p').count(),
        'category_count': Category.objects.count(),
        'tag_count': Tag.objects.count(),
        'comment_count': Comment.objects.filter(is_approved=True).count(),
        'total_views': Article.objects.filter(status='p').aggregate(total=models.Sum('views'))['total'] or 0
    }
    return Response(data)
