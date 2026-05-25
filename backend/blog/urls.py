from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, TagViewSet, ArticleViewSet,
    CommentViewSet, FriendlyLinkViewSet, PersonalLinkViewSet,
    site_settings, statistics
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'friendly-links', FriendlyLinkViewSet, basename='friendlylink')
router.register(r'personal-links', PersonalLinkViewSet, basename='personallink')

urlpatterns = [
    path('', include(router.urls)),
    path('site-settings/', site_settings, name='site-settings'),
    path('statistics/', statistics, name='statistics'),
]
