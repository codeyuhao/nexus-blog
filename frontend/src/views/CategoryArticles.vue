<template>
  <MainLayout>
    <div class="page">
      <header class="page-header">
        <span class="page-label">分类</span>
        <h1 class="page-title">{{ catName || '加载中...' }}</h1>
      </header>
      <div class="articles-list">
        <article
          v-for="(item, i) in articles"
          :key="item.id"
          class="list-item reveal"
          :style="{ animationDelay: `${i * 0.06}s` }"
          @click="$router.push(`/article/${item.id}`)"
        >
          <div class="item-img" :style="{ backgroundImage: item.cover_image ? `url(${item.cover_image})` : '' }"></div>
          <div class="item-body">
            <div class="item-meta">
              <span>{{ formatDate(item.created_at) }}</span>
            </div>
            <h3 class="item-title">{{ item.title }}</h3>
            <p class="item-desc" v-if="item.summary">{{ item.summary.slice(0, 120) }}{{ item.summary.length > 120 ? '...' : '' }}</p>
          </div>
        </article>
        <p class="empty-state" v-if="!articles.length && !loading">该分类暂无文章</p>
        <div class="loading-spinner" v-if="loading"></div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getArticles, getCategories } from '@/api'
import MainLayout from '@/layouts/MainLayout.vue'

const route = useRoute()
const articles = ref([])
const catName = ref('')
const loading = ref(true)

const formatDate = (d) => {
  const date = new Date(d)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

onMounted(async () => {
  try {
    const [cats, arts] = await Promise.all([
      getCategories(),
      getArticles({ category: route.params.id })
    ])
    const clist = Array.isArray(cats) ? cats : (cats.results || [])
    const found = clist.find(c => c.id == route.params.id)
    catName.value = found?.name || ''
    articles.value = Array.isArray(arts) ? arts : (arts.results || [])
  } catch { articles.value = [] }
  finally { loading.value = false }
})
</script>

<style scoped>
.page {
  max-width: 800px;
  margin: 0 auto;
  padding: 80px 24px 80px;
}

.page-header {
  margin-bottom: 48px;
}

.page-label {
  display: block;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 10px;
}

.page-title {
  font-size: 36px;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.articles-list {
  display: flex;
  flex-direction: column;
}

.list-item {
  display: flex;
  gap: 24px;
  padding: 28px 0;
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.25s;
}

.list-item:first-child {
  padding-top: 0;
}

.list-item:hover {
  opacity: 0.8;
}

.item-img {
  width: 180px;
  flex-shrink: 0;
  aspect-ratio: 16 / 10;
  background: linear-gradient(135deg, #eef2ff, #f3f0ff);
  background-size: cover;
  background-position: center;
  border-radius: var(--radius-sm);
  transition: transform 0.4s var(--ease-out);
}

.list-item:hover .item-img {
  transform: scale(1.04);
}

.item-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.item-meta {
  font-size: 13px;
  color: var(--text-tertiary);
  margin-bottom: 8px;
}

.item-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 8px;
}

.item-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

.empty-state {
  text-align: center;
  color: var(--text-tertiary);
  padding: 80px 0;
}

@media (max-width: 640px) {
  .page {
    padding: 60px 16px 60px;
  }

  .list-item {
    flex-direction: column;
    gap: 16px;
  }

  .item-img {
    width: 100%;
  }
}
</style>