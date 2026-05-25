<template>
  <article class="article-card" @click="$router.push(`/article/${article.id}`)">
    <div class="card-cover">
      <div
        class="card-img"
        :style="{ backgroundImage: article.cover_image ? `url(${article.cover_image})` : '' }"
      >
        <div class="card-img-placeholder" v-if="!article.cover_image">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
            <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
        </div>
      </div>
      <div class="card-cat" v-if="article.category">
        {{ article.category.name }}
      </div>
    </div>
    <div class="card-body">
      <div class="card-meta">
        <span>{{ formatDate(article.created_at) }}</span>
        <span class="meta-dot"></span>
        <span>{{ article.views || 0 }} 阅读</span>
      </div>
      <h3 class="card-title">{{ article.title }}</h3>
      <p class="card-desc" v-if="article.summary">{{ article.summary.slice(0, 100) }}{{ article.summary.length > 100 ? '...' : '' }}</p>
      <div class="card-tags" v-if="article.tags?.length">
        <span v-for="t in article.tags.slice(0, 3)" :key="t.id" class="card-tag">{{ t.name }}</span>
      </div>
    </div>
  </article>
</template>

<script setup>
const props = defineProps({
  article: { type: Object, required: true },
  index: { type: Number, default: 0 }
})

const formatDate = (d) => {
  const date = new Date(d)
  return date.toLocaleDateString('zh-CN', { month: 'long', day: 'numeric' })
}
</script>

<style scoped>
.article-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.35s var(--ease-out);
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
  border-color: transparent;
}

.card-cover {
  position: relative;
}

.card-img {
  aspect-ratio: 16 / 10;
  background: linear-gradient(135deg, #eef2ff 0%, #f3f0ff 100%);
  background-size: cover;
  background-position: center;
  transition: transform 0.5s var(--ease-out);
}

.article-card:hover .card-img {
  transform: scale(1.04);
}

.card-img-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
  opacity: 0.5;
}

.card-cat {
  position: absolute;
  top: 14px;
  left: 14px;
  padding: 5px 12px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  color: var(--accent);
  box-shadow: var(--shadow-sm);
}

.card-body {
  padding: 20px 22px 22px;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: var(--text-tertiary);
  margin-bottom: 10px;
}

.meta-dot {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: var(--text-tertiary);
}

.card-title {
  font-size: 18px;
  font-weight: 700;
  line-height: 1.4;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.2s;
}

.article-card:hover .card-title {
  color: var(--accent);
}

.card-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.card-tag {
  padding: 3px 10px;
  background: var(--bg-secondary);
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
}
</style>