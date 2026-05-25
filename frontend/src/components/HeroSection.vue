<template>
  <section class="hero">
    <div class="hero-pattern"></div>
    <div class="hero-content">
      <div class="hero-label">精选推荐</div>
      <h1 class="hero-title" v-if="article">
        <router-link :to="`/article/${article.id}`">
          {{ article.title }}
        </router-link>
      </h1>
      <p class="hero-desc" v-if="article?.summary">
        {{ article.summary.slice(0, 150) }}{{ article.summary.length > 150 ? '...' : '' }}
      </p>
      <div class="hero-meta" v-if="article">
        <span class="hero-meta-item">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          {{ formatDate(article.created_at) }}
        </span>
        <span class="hero-meta-item" v-if="article.category">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
          {{ article.category.name }}
        </span>
        <span class="hero-meta-item">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
          {{ article.views || 0 }} 次阅读
        </span>
      </div>
      <router-link v-if="article" :to="`/article/${article.id}`" class="hero-cta">
        阅读全文
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
      </router-link>
    </div>
    <div class="hero-empty" v-if="!article">
      <div class="hero-label">欢迎来到</div>
      <h1 class="hero-title">Nexus Blog</h1>
      <p class="hero-desc">还没有发布文章，请在后台管理中创建第一篇博文。</p>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  article: { type: Object, default: null }
})

const formatDate = (d) => {
  const date = new Date(d)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}
</script>

<style scoped>
.hero {
  position: relative;
  padding: 120px 24px 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 520px;
  overflow: hidden;
}

.hero-pattern {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 50% 0%, rgba(99, 102, 241, 0.06) 0%, transparent 60%),
    radial-gradient(ellipse 60% 50% at 80% 80%, rgba(168, 85, 247, 0.04) 0%, transparent 60%);
  pointer-events: none;
}

.hero-content,
.hero-empty {
  position: relative;
  z-index: 1;
  max-width: 720px;
  text-align: center;
}

.hero-label {
  display: inline-block;
  padding: 6px 18px;
  background: var(--accent-soft);
  color: var(--accent);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.08em;
  border-radius: 20px;
  margin-bottom: 24px;
}

.hero-title {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -0.03em;
  margin-bottom: 20px;
}

.hero-title a {
  transition: opacity 0.3s;
}

.hero-title a:hover {
  opacity: 0.75;
}

.hero-desc {
  font-size: 17px;
  color: var(--text-secondary);
  line-height: 1.75;
  max-width: 560px;
  margin: 0 auto 28px;
}

.hero-meta {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 36px;
  flex-wrap: wrap;
}

.hero-meta-item {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 14px;
  color: var(--text-tertiary);
}

.hero-meta-item svg {
  flex-shrink: 0;
}

.hero-cta {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 32px;
  background: var(--text-primary);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  border-radius: 12px;
  transition: all 0.3s var(--ease-out);
  box-shadow: var(--shadow-md);
}

.hero-cta:hover {
  background: var(--accent);
  box-shadow: var(--shadow-glow);
  transform: translateY(-2px);
}

.hero-empty .hero-title {
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

@media (max-width: 640px) {
  .hero {
    padding: 100px 16px 60px;
    min-height: 400px;
  }

  .hero-meta {
    gap: 16px;
  }
}
</style>