<template>
  <MainLayout>
    <HeroSection :article="featured" />
    <section class="content-section">
      <div class="section-header">
        <h2 class="section-title">最新文章</h2>
        <div class="section-line"></div>
        <span class="section-count" v-if="articles.length">{{ articles.length }} 篇</span>
      </div>
      <div class="articles-grid">
        <ArticleCard
          v-for="(article, i) in articles"
          :key="article.id"
          :article="article"
          :index="i + 1"
          class="reveal"
          :style="{ animationDelay: `${i * 0.07}s` }"
        />
      </div>
      <div class="load-more-wrap" v-if="hasMore">
        <button class="load-more-btn" @click="loadMore" :disabled="loading">
          <span v-if="loading" class="loading-spinner"></span>
          <span v-else>加载更多文章</span>
        </button>
      </div>
      <div class="empty-state" v-if="!loading && articles.length === 0 && !featured">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
          <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
          <polyline points="14 2 14 8 20 8"/>
        </svg>
        <p>暂无已发布的文章</p>
      </div>
    </section>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getArticles } from '@/api'
import MainLayout from '@/layouts/MainLayout.vue'
import HeroSection from '@/components/HeroSection.vue'
import ArticleCard from '@/components/ArticleCard.vue'

const allArticles = ref([])
const loading = ref(false)
const page = ref(1)
const hasMore = ref(true)

const featured = computed(() => allArticles.value[0] || null)
const articles = computed(() => {
  if (!allArticles.value.length) return []
  return featured.value ? allArticles.value.slice(1) : allArticles.value
})

const fetchArticles = async (p = 1, append = false) => {
  loading.value = true
  try {
    const data = await getArticles({ page: p, page_size: 11 })
    const results = Array.isArray(data) ? data : (data.results || [])
    allArticles.value = append ? [...allArticles.value, ...results] : results
    hasMore.value = results.length >= 10
  } catch {
    if (!append) allArticles.value = []
  } finally {
    loading.value = false
  }
}

const loadMore = () => {
  page.value++
  fetchArticles(page.value, true)
}

onMounted(() => fetchArticles())
</script>

<style scoped>
.content-section {
  max-width: var(--content-width);
  margin: 0 auto;
  padding: 20px 24px 80px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 40px;
}

.section-title {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-tertiary);
  white-space: nowrap;
}

.section-line {
  flex: 1;
  height: 1px;
  background: var(--border-color);
}

.section-count {
  font-size: 13px;
  color: var(--text-tertiary);
  white-space: nowrap;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 28px;
}

.load-more-wrap {
  text-align: center;
  margin-top: 56px;
}

.load-more-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 180px;
  padding: 14px 36px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.25s;
}

.load-more-btn:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent);
  box-shadow: var(--shadow-sm);
}

.load-more-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.empty-state {
  text-align: center;
  padding: 80px 0;
  color: var(--text-tertiary);
}

.empty-state svg {
  margin: 0 auto 16px;
  opacity: 0.4;
}

.empty-state p {
  font-size: 15px;
}

@media (max-width: 640px) {
  .articles-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .content-section {
    padding: 20px 16px 60px;
  }
}
</style>