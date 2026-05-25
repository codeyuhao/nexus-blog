from django.contrib import admin
from django.db.models import Count
from django.utils.html import mark_safe
from .models import Category, Tag, Article, Comment, FriendlyLink, PersonalLink, SiteSettings


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'article_count_badge', 'description_preview', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20

    @admin.display(description='文章数')
    def article_count_badge(self, obj):
        count = getattr(obj, '_annotated_article_count', None)
        if count is None:
            count = obj.article_set.count()
        return mark_safe(
            f'<span style="display:inline-block;background:#eef2ff;color:#6366f1;padding:3px 12px;border-radius:12px;font-weight:600;font-size:13px;">{count}</span>'
        )

    @admin.display(description='描述')
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:40] + ('...' if len(obj.description) > 40 else '')
        return '-'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_annotated_article_count=Count('article'))


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 30


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status_badge', 'is_top_badge', 'views', 'comment_count_badge', 'created_at']
    list_filter = ['status', 'is_top', 'category', 'tags', 'created_at']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    list_editable = []
    date_hierarchy = 'created_at'
    save_on_top = True
    list_per_page = 20

    fieldsets = [
        ('基本信息', {
            'fields': ('title', 'slug', 'category', 'tags', 'status', 'is_top', 'cover_image'),
            'description': '填写文章的基本信息，包括标题、分类和标签'
        }),
        ('正文内容', {
            'fields': ('summary', 'content'),
            'classes': ('wide',),
            'description': '摘要会在文章列表和卡片中展示，正文支持 Markdown 格式'
        }),
        ('数据统计', {
            'fields': ('views', 'created_at'),
            'classes': ('collapse',),
            'description': '浏览量和创建时间，由系统自动维护'
        }),
    ]
    readonly_fields = ['views', 'created_at']

    @admin.display(description='状态')
    def status_badge(self, obj):
        if obj.status == 'p':
            return mark_safe(
                '<span style="display:inline-block;background:#dcfce7;color:#16a34a;padding:4px 12px;border-radius:12px;font-weight:600;font-size:12px;">已发布</span>'
            )
        return mark_safe(
            '<span style="display:inline-block;background:#fef3c7;color:#d97706;padding:4px 12px;border-radius:12px;font-weight:600;font-size:12px;">草稿</span>'
        )

    @admin.display(description='置顶')
    def is_top_badge(self, obj):
        if obj.is_top:
            return mark_safe(
                '<span style="display:inline-block;background:#fce7f3;color:#db2777;padding:4px 12px;border-radius:12px;font-weight:600;font-size:12px;">置顶</span>'
            )
        return mark_safe('<span style="color:#d1d5db;">—</span>')

    @admin.display(description='评论')
    def comment_count_badge(self, obj):
        count = obj.comment_set.count()
        return mark_safe(
            f'<span style="display:inline-block;background:#f3f4f6;color:#6b7280;padding:3px 12px;border-radius:12px;font-weight:600;font-size:13px;">{count}</span>'
        )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'article_link', 'content_preview', 'approved_badge', 'created_at']
    list_filter = ['is_approved', 'created_at', 'article']
    search_fields = ['author_name', 'author_email', 'content']
    list_editable = []
    date_hierarchy = 'created_at'
    actions = ['approve_comments', 'unapprove_comments']
    list_per_page = 30

    @admin.display(description='文章')
    def article_link(self, obj):
        title = obj.article.title[:25] + ('...' if len(obj.article.title) > 25 else '')
        return mark_safe(
            f'<a href="/admin/blog/article/{obj.article_id}/change/" style="color:#6366f1;font-weight:600;">{title}</a>'
        )

    @admin.display(description='内容')
    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')

    @admin.display(description='状态')
    def approved_badge(self, obj):
        if obj.is_approved:
            return mark_safe(
                '<span style="display:inline-block;background:#dcfce7;color:#16a34a;padding:4px 12px;border-radius:12px;font-weight:600;font-size:12px;">已通过</span>'
            )
        return mark_safe(
            '<span style="display:inline-block;background:#fee2e2;color:#dc2626;padding:4px 12px;border-radius:12px;font-weight:600;font-size:12px;">待审核</span>'
        )

    @admin.action(description='通过选中的评论')
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'已通过 {updated} 条评论')

    @admin.action(description='取消通过选中的评论')
    def unapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'已取消 {updated} 条评论的通过状态')


@admin.register(FriendlyLink)
class FriendlyLinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'url_preview', 'logo_preview', 'active_badge', 'sort_order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'url', 'description']
    list_editable = ['sort_order']
    list_per_page = 20

    @admin.display(description='链接')
    def url_preview(self, obj):
        url = obj.url[:35] + ('...' if len(obj.url) > 35 else '')
        return mark_safe(f'<a href="{obj.url}" target="_blank" style="color:#6366f1;">{url}</a>')

    @admin.display(description='Logo')
    def logo_preview(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo}" style="width:28px;height:28px;border-radius:6px;object-fit:cover;" />')
        return mark_safe('<span style="color:#d1d5db;">—</span>')

    @admin.display(description='状态')
    def active_badge(self, obj):
        if obj.is_active:
            return mark_safe(
                '<span style="display:inline-block;background:#dcfce7;color:#16a34a;padding:4px 12px;border-radius:12px;font-weight:600;font-size:12px;">激活</span>'
            )
        return mark_safe(
            '<span style="display:inline-block;background:#f3f4f6;color:#9ca3af;padding:4px 12px;border-radius:12px;font-weight:600;font-size:12px;">停用</span>'
        )


@admin.register(PersonalLink)
class PersonalLinkAdmin(admin.ModelAdmin):
    list_display = ['platform_display', 'name', 'url_preview', 'sort_order', 'active_badge']
    list_filter = ['platform', 'is_active']
    search_fields = ['name', 'url']
    list_editable = ['sort_order']
    list_per_page = 20

    @admin.display(description='平台')
    def platform_display(self, obj):
        colors = {
            'github': '#333', 'gitee': '#c71d23', 'zhihu': '#0066ff',
            'weibo': '#e6162d', 'bilibili': '#fb7299', 'twitter': '#1da1f2',
            'linkedin': '#0a66c2', 'wechat': '#07c160', 'other': '#6b7280',
        }
        color = colors.get(obj.platform, '#6b7280')
        return mark_safe(
            f'<span style="display:inline-flex;align-items:center;gap:6px;font-weight:600;font-size:13px;">'
            f'<span style="width:8px;height:8px;border-radius:50%;background:{color};"></span>'
            f'{obj.get_platform_display()}</span>'
        )

    @admin.display(description='链接')
    def url_preview(self, obj):
        url = obj.url[:30] + ('...' if len(obj.url) > 30 else '')
        return mark_safe(f'<a href="{obj.url}" target="_blank" style="color:#6366f1;">{url}</a>')

    @admin.display(description='状态')
    def active_badge(self, obj):
        if obj.is_active:
            return mark_safe(
                '<span style="display:inline-block;background:#dcfce7;color:#16a34a;padding:4px 12px;border-radius:12px;font-weight:600;font-size:12px;">激活</span>'
            )
        return mark_safe(
            '<span style="display:inline-block;background:#f3f4f6;color:#9ca3af;padding:4px 12px;border-radius:12px;font-weight:600;font-size:12px;">停用</span>'
        )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_description_preview']

    @admin.display(description='简介')
    def site_description_preview(self, obj):
        if obj.site_description:
            return obj.site_description[:50] + ('...' if len(obj.site_description) > 50 else '')
        return '-'

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


admin.site.site_header = 'Nexus 管理后台'
admin.site.site_title = 'Nexus Blog'
admin.site.index_title = '控制台'
admin.site.enable_nav_sidebar = True