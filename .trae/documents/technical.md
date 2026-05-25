## 1. 架构设计

前端采用纯 Vue 3 + Vite 架构，后端保持不变为 Django 6 + DRF。前端使用原生 CSS 变量 + CSS Grid/Flexbox 实现，不依赖任何 UI 框架（如 Element Plus），确保完全的自定义设计控制权。

## 2. 技术描述

- 前端：Vue 3 + Vite + 原生 CSS
- 字体：Plus Jakarta Sans（Google Fonts，标题）+ JetBrains Mono（代码）
- 动画：纯 CSS @keyframes + CSS transitions
- 图标：SVG inline icons（不依赖图标库）
- 后端：Django 6 + DRF（保持不变）
- 数据库：SQLite/MySQL（现有配置不变）

## 3. 路由定义

| 路由 | 页面 | 说明 |
|------|------|------|
| / | Home | 首页英雄区+文章网格 |
| /article/:id | Article | 文章详情+评论区 |
| /category | Categories | 分类网格 |
| /category/:id | CategoryArticles | 按分类筛选 |
| /tag | Tags | 标签云 |
| /tag/:id | TagArticles | 按标签筛选 |
| /search | Search | 搜索结果 |
| /about | About | 关于页 |

## 4. CSS 变量系统

```css
:root {
  --bg-primary: #0a0a12;
  --bg-secondary: #111118;
  --bg-card: rgba(255, 255, 255, 0.04);
  --bg-card-hover: rgba(255, 255, 255, 0.07);
  --text-primary: #e8e8ed;
  --text-secondary: #9090a0;
  --neon-cyan: #00f0ff;
  --neon-magenta: #ff00e5;
  --neon-cyan-dim: rgba(0, 240, 255, 0.15);
  --neon-magenta-dim: rgba(255, 0, 229, 0.12);
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-glow: rgba(0, 240, 255, 0.25);
  --font-heading: 'Plus Jakarta Sans', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --shadow-glow-cyan: 0 0 30px rgba(0, 240, 255, 0.2);
  --shadow-glow-magenta: 0 0 30px rgba(255, 0, 229, 0.2);
}
```

## 5. 组件结构

- `src/App.vue` - 根组件
- `src/layouts/MainLayout.vue` - 主布局（Header+Footer+router-view）
- `src/components/AppHeader.vue` - 导航栏（含滚动状态切换）
- `src/components/AppFooter.vue` - 页脚
- `src/components/ArticleCard.vue` - 文章卡片（毛玻璃+霓虹悬浮）
- `src/components/HeroSection.vue` - 首页英雄区
- `src/views/HomePage.vue` - 首页
- `src/views/ArticlePage.vue` - 文章详情页
- `src/views/CategoriesPage.vue` - 分类列表
- `src/views/TagsPage.vue` - 标签页
- `src/views/SearchPage.vue` - 搜索结果
- `src/views/AboutPage.vue` - 关于页