from django.db import models
from django.utils import timezone
from markdown import markdown


class Category(models.Model):
    name = models.CharField('分类名称', max_length=100)
    slug = models.SlugField('别名', unique=True)
    description = models.TextField('描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def article_count(self):
        return self.article_set.count()


class Tag(models.Model):
    name = models.CharField('标签名称', max_length=100)
    slug = models.SlugField('别名', unique=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = [
        ('d', '草稿'),
        ('p', '已发布'),
    ]

    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('别名', unique=True, max_length=200)
    summary = models.TextField('摘要', blank=True)
    content = models.TextField('正文')
    content_html = models.TextField('正文HTML', editable=False, blank=True)
    cover_image = models.URLField('封面图片URL', blank=True, null=True)
    status = models.CharField('状态', max_length=1, choices=STATUS_CHOICES, default='p')
    views = models.PositiveIntegerField('浏览量', default=0)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    is_top = models.BooleanField('是否置顶', default=False)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-is_top', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.content_html = markdown(self.content, extensions=['extra', 'codehilite', 'toc'])
        super().save(*args, **kwargs)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def comment_count(self):
        return self.comment_set.count()


class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name='文章', on_delete=models.CASCADE)
    author_name = models.CharField('昵称', max_length=100)
    author_email = models.EmailField('邮箱', max_length=255)
    author_url = models.URLField('网站', blank=True, null=True)
    content = models.TextField('评论内容')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    is_approved = models.BooleanField('是否审核通过', default=True)
    parent = models.ForeignKey('self', verbose_name='父评论', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name} - {self.content[:20]}'


class FriendlyLink(models.Model):
    name = models.CharField('网站名称', max_length=100)
    url = models.URLField('网站地址')
    description = models.TextField('网站描述', blank=True)
    logo = models.URLField('Logo地址', blank=True, null=True)
    is_active = models.BooleanField('是否激活', default=True)
    sort_order = models.IntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name


class PersonalLink(models.Model):
    PLATFORM_CHOICES = [
        ('github', 'GitHub'),
        ('gitee', 'Gitee'),
        ('zhihu', '知乎'),
        ('weibo', '微博'),
        ('bilibili', 'B站'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('wechat', '微信公众号'),
        ('other', '其他'),
    ]

    platform = models.CharField('平台', max_length=20, choices=PLATFORM_CHOICES, default='github')
    name = models.CharField('显示名称', max_length=100, blank=True)
    url = models.URLField('链接地址')
    icon = models.CharField('图标类名', max_length=50, blank=True, help_text='FontAwesome或Element Plus图标类名')
    sort_order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否激活', default=True)

    class Meta:
        verbose_name = '个人链接'
        verbose_name_plural = verbose_name
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.get_platform_display() or self.name


class SiteSettings(models.Model):
    site_name = models.CharField('网站名称', max_length=100, default='我的个人博客')
    site_description = models.TextField('网站描述', blank=True)
    site_keywords = models.CharField('网站关键词', max_length=500, blank=True)
    github_url = models.URLField('GitHub地址', blank=True, null=True)
    avatar = models.URLField('头像URL', blank=True, null=True)
    about_content = models.TextField('关于页面内容', blank=True)

    class Meta:
        verbose_name = '网站设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.site_name
