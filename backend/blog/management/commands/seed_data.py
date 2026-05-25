from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from blog.models import Category, Tag, Article, Comment, FriendlyLink, PersonalLink, SiteSettings


class Command(BaseCommand):
    help = '初始化演示数据'

    def handle(self, *args, **options):
        self.stdout.write('开始创建演示数据...')

        self.create_superuser()
        self.create_site_settings()
        self.create_categories()
        self.create_tags()
        self.create_articles()
        self.create_comments()
        self.create_friendly_links()
        self.create_personal_links()

        self.stdout.write(self.style.SUCCESS('演示数据创建完成！'))

    def create_superuser(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexus.com', 'admin123')
            self.stdout.write('  管理员账号已创建: admin / admin123')
        else:
            self.stdout.write('  管理员账号已存在')

    def create_site_settings(self):
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                site_name='Nexus Blog',
                site_description='一个关于技术、设计与生活的个人博客，分享编程经验与技术见解。',
                site_keywords='博客,技术,Python,Django,Vue,前端,后端,编程',
                github_url='https://github.com',
                about_content='热爱技术与写作的全栈开发者，专注于 Web 开发和开源项目。'
            )
            self.stdout.write('  网站设置已创建')

    def create_categories(self):
        cats = [
            {'name': '前端开发', 'slug': 'frontend', 'description': 'HTML、CSS、JavaScript、Vue、React 等前端技术文章'},
            {'name': '后端开发', 'slug': 'backend', 'description': 'Python、Django、Node.js、Go 等后端技术分享'},
            {'name': '人工智能', 'slug': 'ai', 'description': '机器学习、深度学习、大语言模型等 AI 技术探索'},
            {'name': '工具推荐', 'slug': 'tools', 'description': '好用的开发工具、效率软件和实用插件推荐'},
            {'name': '生活随笔', 'slug': 'life', 'description': '读书笔记、旅行见闻、生活感悟'},
            {'name': '教程指南', 'slug': 'tutorials', 'description': '实用的编程教程和操作指南'},
        ]
        for c in cats:
            if not Category.objects.filter(slug=c['slug']).exists():
                Category.objects.create(**c)
        self.stdout.write(f'  已创建 {len(cats)} 个分类')

    def create_tags(self):
        tags = [
            'Python', 'Django', 'Vue.js', 'React', 'JavaScript',
            'TypeScript', 'CSS', 'Docker', 'Git', 'Linux',
            'MySQL', 'Redis', 'Nginx', 'RESTful API', 'Markdown',
            'Vite', 'Webpack', 'Node.js', '机器学习', '深度学习',
            'ChatGPT', 'LLM', 'Prompt Engineering', 'DevOps', 'CI/CD',
        ]
        created = 0
        for t in tags:
            if not Tag.objects.filter(name=t).exists():
                Tag.objects.create(name=t, slug=t.lower().replace('.', '-').replace(' ', '-'))
                created += 1
        self.stdout.write(f'  已创建 {created} 个标签')

    def create_articles(self):
        if Article.objects.exists():
            self.stdout.write('  文章已存在，跳过创建')
            return

        now = timezone.now()
        articles_data = [
            {
                'title': '使用 Django REST Framework 构建高性能 API',
                'slug': 'django-rest-framework-api',
                'summary': '深入探讨如何使用 Django REST Framework 构建可扩展、高性能的 RESTful API，涵盖序列化、视图集、认证和性能优化。',
                'content': '''# 使用 Django REST Framework 构建高性能 API

Django REST Framework（DRF）是 Django 生态中最流行的 API 框架之一。本文将深入探讨如何构建生产级别的 RESTful API。

## 为什么选择 DRF？

DRF 提供了开箱即用的功能：

- **序列化器（Serializers）**：强大的数据验证和转换
- **视图集（ViewSets）**：减少样板代码
- **认证系统**：内置 Token、Session、JWT 支持
- **权限控制**：细粒度的访问控制

## 项目结构最佳实践

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(status='published')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

## 性能优化技巧

### 1. 使用 select_related 和 prefetch_related

```python
queryset = Article.objects.select_related('author').prefetch_related('tags')
```

### 2. 添加缓存层

对于读多写少的场景，缓存可以显著提升性能：

```python
from django.core.cache import cache

def get_article(article_id):
    key = f'article:{article_id}'
    article = cache.get(key)
    if not article:
        article = Article.objects.get(id=article_id)
        cache.set(key, article, 3600)
    return article
```

### 3. 分页处理

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

## 总结

DRF 是一个成熟且强大的框架，合理使用可以快速构建出高性能的 API 服务。

> 记住：过早优化是万恶之源，先让代码工作，再让它变快。
''',
                'category_slug': 'backend',
                'tags': ['Python', 'Django', 'RESTful API'],
                'status': 'p',
                'views': 1280,
                'is_top': True,
                'created_at': now - timedelta(days=2),
            },
            {
                'title': 'Vue 3 Composition API 实战指南',
                'slug': 'vue3-composition-api-guide',
                'summary': '从 Options API 到 Composition API，通过实战案例掌握 Vue 3 的核心特性：ref、reactive、computed 和 watch。',
                'content': '''# Vue 3 Composition API 实战指南

Vue 3 引入的 Composition API 彻底改变了我们组织组件逻辑的方式。

## 为什么需要 Composition API？

在 Options API 中，相关逻辑被分散在 `data`、`methods`、`computed` 等选项中，随着组件复杂度增加，代码维护变得困难。

Composition API 允许我们**按逻辑关注点**组织代码。

## 核心概念

### ref 与 reactive

```javascript
import { ref, reactive } from 'vue'

// ref 用于基本类型
const count = ref(0)
const message = ref('Hello')

// reactive 用于对象
const state = reactive({
  user: null,
  loading: false
})
```

### 组合函数（Composables）

这是 Composition API 的精髓所在：

```javascript
// useCounter.js
import { ref, computed } from 'vue'

export function useCounter(initialValue = 0) {
  const count = ref(initialValue)
  const doubled = computed(() => count.value * 2)

  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  return { count, doubled, increment, decrement }
}
```

### watch 与 watchEffect

```javascript
// 监听特定数据源
watch(count, (newVal, oldVal) => {
  console.log(`count changed from ${oldVal} to ${newVal}`)
})

// 自动追踪依赖
watchEffect(() => {
  console.log(`Current count: ${count.value}`)
})
```

## 实战：搜索组件

```vue
<script setup>
import { ref, watch } from 'vue'

const keyword = ref('')
const results = ref([])
const loading = ref(false)

let timer = null

watch(keyword, (val) => {
  if (timer) clearTimeout(timer)
  timer = setTimeout(async () => {
    if (val.length < 2) {
      results.value = []
      return
    }
    loading.value = true
    results.value = await fetchResults(val)
    loading.value = false
  }, 300)
})
</script>
```

## 总结

Composition API 不是 Options API 的替代品，而是另一种选择。对于简单组件，Options API 依然简洁；对于复杂逻辑，Composition API 让代码更易维护。
''',
                'category_slug': 'frontend',
                'tags': ['Vue.js', 'JavaScript', 'TypeScript'],
                'status': 'p',
                'views': 960,
                'is_top': False,
                'created_at': now - timedelta(days=5),
            },
            {
                'title': 'Docker 容器化部署实战：从零到生产',
                'slug': 'docker-deployment-guide',
                'summary': '一份完整的 Docker 部署指南，涵盖 Dockerfile 编写、docker-compose 编排、多阶段构建和 CI/CD 集成。',
                'content': '''# Docker 容器化部署实战：从零到生产

容器化已经成为现代应用部署的标准方案。本文将带你从零开始掌握 Docker 部署。

## Docker 基础概念

- **镜像（Image）**：应用的只读模板
- **容器（Container）**：镜像的运行实例
- **Dockerfile**：构建镜像的脚本
- **Docker Compose**：多容器应用编排工具

## 编写最佳实践的 Dockerfile

```dockerfile
# 多阶段构建
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]
```

多阶段构建可以显著减小最终镜像的体积。

## Docker Compose 编排

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
    volumes:
      - ./media:/app/media

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

## CI/CD 集成

在 GitHub Actions 中自动构建和推送镜像：

```yaml
- name: Build and push
  uses: docker/build-push-action@v4
  with:
    context: .
    push: true
    tags: ${{ secrets.DOCKER_USERNAME }}/app:latest
```

## 生产环境 Checklist

1. 使用非 root 用户运行容器
2. 限制容器资源（CPU、内存）
3. 配置健康检查
4. 启用日志收集
5. 使用 secrets 管理敏感信息

Docker 让部署变得简单可靠，是现代开发的必备技能。
''',
                'category_slug': 'tools',
                'tags': ['Docker', 'DevOps', 'CI/CD', 'Linux'],
                'status': 'p',
                'views': 756,
                'is_top': False,
                'created_at': now - timedelta(days=8),
            },
            {
                'title': '深入理解 JavaScript 异步编程',
                'slug': 'javascript-async-programming',
                'summary': '从回调函数到 Promise，再到 async/await，全面解析 JavaScript 异步编程模式的演进与最佳实践。',
                'content': '''# 深入理解 JavaScript 异步编程

JavaScript 的异步编程模型经历了从回调到 Promise 再到 async/await 的演进。

## 回调地狱

早期的异步编程依赖回调函数，嵌套过深会导致"回调地狱"：

```javascript
getData(function(a) {
  getMoreData(a, function(b) {
    getEvenMoreData(b, function(c) {
      console.log(c)
    })
  })
})
```

## Promise 时代

Promise 提供了链式调用，大幅改善了代码可读性：

```javascript
getData()
  .then(a => getMoreData(a))
  .then(b => getEvenMoreData(b))
  .then(c => console.log(c))
  .catch(err => console.error(err))
```

### Promise 静态方法

```javascript
// 并行执行
const [user, posts] = await Promise.all([
  fetchUser(),
  fetchPosts()
])

// 竞速
const result = await Promise.race([
  fetch(url),
  timeout(5000)
])
```

## async/await 现代方案

async/await 是异步编程的语法糖，让异步代码看起来像同步代码：

```javascript
async function loadDashboard() {
  try {
    const user = await fetchUser()
    const posts = await fetchPosts(user.id)
    const stats = await fetchStats()
    return { user, posts, stats }
  } catch (error) {
    console.error('Failed to load dashboard:', error)
    throw error
  }
}
```

## 错误处理模式

```javascript
// 包装模式，避免 try-catch 嵌套
async function to(promise) {
  return promise
    .then(data => [null, data])
    .catch(err => [err, null])
}

const [err, user] = await to(fetchUser())
if (err) return handleError(err)
```

理解异步编程是成为高级 JavaScript 开发者的必经之路。
''',
                'category_slug': 'frontend',
                'tags': ['JavaScript', 'Node.js'],
                'status': 'p',
                'views': 543,
                'is_top': False,
                'created_at': now - timedelta(days=12),
            },
            {
                'title': 'Python 代码质量提升：从 Lint 到自动化测试',
                'slug': 'python-code-quality',
                'summary': '如何通过类型注解、代码检查工具和自动化测试体系，打造高质量的 Python 项目。',
                'content': '''# Python 代码质量提升：从 Lint 到自动化测试

代码质量决定了项目的长期可维护性。本文将介绍提升 Python 代码质量的实践。

## 类型注解

Python 3.6+ 支持类型注解，配合 mypy 可以在运行前发现类型错误：

```python
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class Article:
    title: str
    content: str
    author_id: int
    tags: List[str]
    summary: Optional[str] = None
```

## 代码格式化

使用 Black 统一代码风格，isort 管理导入顺序：

```bash
pip install black isort
black .
isort .
```

配置 pre-commit hook 自动化代码检查：

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.0.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
```

## 测试金字塔

### 单元测试

```python
import pytest
from app.services import ArticleService

def test_create_article_success():
    service = ArticleService()
    article = service.create("Test", "Content", 1)
    assert article.title == "Test"
    assert article.status == "published"
```

### 集成测试

```python
def test_api_create_article(client):
    response = client.post('/api/articles/', json={
        'title': 'Test',
        'content': 'Hello World'
    })
    assert response.status_code == 201
```

## CI 配置

在 GitHub Actions 中运行完整的检查流水线：

```yaml
- name: Run checks
  run: |
    black --check .
    isort --check .
    mypy .
    pytest --cov=. --cov-report=xml
```

投入时间建立质量体系，长期回报远超成本。
''',
                'category_slug': 'tutorials',
                'tags': ['Python', 'CI/CD', 'Linux'],
                'status': 'p',
                'views': 432,
                'is_top': False,
                'created_at': now - timedelta(days=15),
            },
            {
                'title': 'CSS Grid 与 Flexbox 布局完全指南',
                'slug': 'css-grid-flexbox-guide',
                'summary': '一文搞懂现代 CSS 布局的两大核心：Grid 和 Flexbox。附大量实用示例和常见布局方案。',
                'content': '''# CSS Grid 与 Flexbox 布局完全指南

现代 CSS 提供了两种强大的布局方案：Flexbox 和 Grid。

## Flexbox：一维布局

Flexbox 适合单一方向的布局——行或列。

### 弹性容器属性

```css
.container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}
```

### 弹性子项属性

```css
.item {
  flex: 1 1 300px; /* grow shrink basis */
  min-width: 0; /* 防止溢出 */
}
```

### 实战：导航栏

```css
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 64px;
}

.nav-links {
  display: flex;
  gap: 24px;
}
```

## CSS Grid：二维布局

Grid 适合行列两个维度的复杂布局。

### 基础语法

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  grid-template-rows: auto;
  gap: 24px;
}
```

### 网格区域

```css
.layout {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main main"
    "footer footer footer";
  grid-template-columns: 250px 1fr 1fr;
  min-height: 100vh;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

## Flexbox vs Grid：如何选择？

| 场景 | 推荐 |
|------|------|
| 导航栏、工具栏 | Flexbox |
| 卡片网格 | Grid |
| 页面整体布局 | Grid |
| 表单行对齐 | Flexbox |
| 居中单个元素 | Flexbox |

两者不是竞争关系，而是互补。掌握它们，90% 的布局问题都能优雅解决。
''',
                'category_slug': 'frontend',
                'tags': ['CSS', 'Vite'],
                'status': 'p',
                'views': 389,
                'is_top': False,
                'created_at': now - timedelta(days=20),
            },
            {
                'title': 'Git 工作流最佳实践',
                'slug': 'git-workflow-best-practices',
                'summary': '团队协作中 Git 工作流的选择与实践，包括 GitFlow、GitHub Flow 和 Trunk-Based Development。',
                'content': '''# Git 工作流最佳实践

选择合适的 Git 工作流对团队协作效率至关重要。

## 三种主流工作流

### GitFlow

适合有固定发布周期的项目：

- `main` - 生产分支
- `develop` - 开发主分支
- `feature/*` - 功能分支
- `release/*` - 发布分支
- `hotfix/*` - 紧急修复分支

### GitHub Flow

适合持续部署的 Web 项目：

1. 从 `main` 创建 feature 分支
2. 提交代码
3. 创建 Pull Request
4. Code Review
5. 合并到 `main` 并自动部署

### Trunk-Based Development

适合成熟的 DevOps 团队：

- 所有人直接向 `main`（trunk）提交
- 通过 feature flag 控制未完成功能
- 极其频繁的集成

## Commit Message 规范

使用 Conventional Commits：

```
feat: 添加用户登录功能
fix: 修复分页计算错误
docs: 更新 API 文档
refactor: 重构认证模块
test: 添加用户服务单元测试
chore: 更新依赖版本
```

## Code Review 要点

- 每次 PR 保持小而专注（< 400 行）
- 写清楚 PR 描述：做了什么、为什么做
- 自动检查先行：lint、test、build
- 至少一人 Approve 后合并

## 实用 Git 技巧

```bash
# 交互式 rebase 整理提交历史
git rebase -i HEAD~5

# 暂存当前工作
git stash push -m "WIP: 搜索功能"

# 挑选特定提交
git cherry-pick abc123

# 撤销最后一次提交但保留更改
git reset --soft HEAD~1
```

好的 Git 习惯让团队协作事半功倍。
''',
                'category_slug': 'tutorials',
                'tags': ['Git', 'DevOps'],
                'status': 'p',
                'views': 312,
                'is_top': False,
                'created_at': now - timedelta(days=25),
            },
        ]

        for data in articles_data:
            category_slug = data.pop('category_slug')
            tags = data.pop('tags')
            status = data.pop('status')
            views = data.pop('views')
            is_top = data.pop('is_top')
            category = Category.objects.get(slug=category_slug)

            article = Article.objects.create(
                **data,
                category=category,
                status=status,
                views=views,
                is_top=is_top,
            )
            for tag_name in tags:
                tag = Tag.objects.get(name=tag_name)
                article.tags.add(tag)

        self.stdout.write(f'  已创建 {len(articles_data)} 篇文章')

    def create_comments(self):
        if Comment.objects.exists():
            self.stdout.write('  评论已存在，跳过创建')
            return

        articles = list(Article.objects.all())
        if not articles:
            return

        comments_data = [
            {'author_name': '技术爱好者', 'author_email': 'fan@example.com', 'content': '写得太好了！Django REST Framework 确实强大，最近在公司项目中也用上了，序列化器和视图集让 API 开发效率提升了不止一倍。希望能看到更多关于性能优化的内容！'},
            {'author_name': '前端小张', 'author_email': 'zhang@example.com', 'content': 'Composition API 真是 Vue 3 最棒的改进，代码组织方式清晰了很多。不过对于简单组件，我还是喜欢用 Options API，更直观一些。'},
            {'author_name': 'DevOps_Leo', 'author_email': 'leo@example.com', 'content': 'Docker 部署部分写得很有条理，多阶段构建那块对我帮助很大。想问一下，在 k8s 环境下部署 Django 应用有什么额外需要注意的吗？'},
            {'author_name': 'Coder_Li', 'author_email': 'li@example.com', 'content': 'async/await 确实让异步代码清爽了很多，但 error handling 还是容易疏忽。文章里提到的 to() 包装函数很实用，已经在用了。'},
            {'author_name': '设计师小王', 'author_email': 'wang@example.com', 'content': '终于看到有人把 Grid 和 Flexbox 的区别讲清楚了！之前一直搞混两者的使用场景，现在完全明白了。'},
            {'author_name': '资深码农', 'author_email': 'coder@example.com', 'content': 'Python 代码质量那篇文章很干货，pre-commit hook 自动化检查是我们团队的标准配置，推荐大家都用起来。'},
            {'author_name': '小小白', 'author_email': 'newbie@example.com', 'content': '刚开始学 Git，Conventional Commits 规范很有帮助。请问有没有可视化工具可以推荐？目前用 VSCode 内置的感觉够用了。'},
            {'author_name': '全栈之路', 'author_email': 'fullstack@example.com', 'content': '系列文章质量都很高，已经收藏了。期待更多实战内容！'},
        ]

        for i, data in enumerate(comments_data):
            Comment.objects.create(
                article=articles[i % len(articles)],
                author_name=data['author_name'],
                author_email=data['author_email'],
                content=data['content'],
                is_approved=True,
            )

        self.stdout.write(f'  已创建 {len(comments_data)} 条评论')

    def create_friendly_links(self):
        if FriendlyLink.objects.exists():
            self.stdout.write('  友情链接已存在，跳过创建')
            return

        links = [
            {'name': 'Python 官方文档', 'url': 'https://docs.python.org/zh-cn/3/', 'description': 'Python 编程语言官方中文文档', 'sort_order': 1},
            {'name': 'Vue.js 中文文档', 'url': 'https://cn.vuejs.org/', 'description': '渐进式 JavaScript 框架中文文档', 'sort_order': 2},
            {'name': 'MDN Web 文档', 'url': 'https://developer.mozilla.org/zh-CN/', 'description': 'Web 开发权威参考资料', 'sort_order': 3},
            {'name': 'GitHub', 'url': 'https://github.com/', 'description': '全球最大的代码托管平台', 'sort_order': 4},
        ]
        for link in links:
            FriendlyLink.objects.create(**link)
        self.stdout.write(f'  已创建 {len(links)} 个友情链接')

    def create_personal_links(self):
        if PersonalLink.objects.exists():
            self.stdout.write('  个人链接已存在，跳过创建')
            return

        links = [
            {'platform': 'github', 'name': 'GitHub', 'url': 'https://github.com/', 'sort_order': 1},
            {'platform': 'zhihu', 'name': '知乎', 'url': 'https://www.zhihu.com/', 'sort_order': 2},
            {'platform': 'bilibili', 'name': 'B站', 'url': 'https://www.bilibili.com/', 'sort_order': 3},
            {'platform': 'twitter', 'name': 'Twitter', 'url': 'https://twitter.com/', 'sort_order': 4},
        ]
        for link in links:
            PersonalLink.objects.create(**link)
        self.stdout.write(f'  已创建 {len(links)} 个个人链接')