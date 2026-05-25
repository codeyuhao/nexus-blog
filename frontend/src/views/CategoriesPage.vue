<template>
  <MainLayout>
    <div class="page">
      <header class="page-header">
        <h1 class="page-title">文章分类</h1>
        <p class="page-sub">浏览不同主题下的文章</p>
      </header>
      <div class="categories-grid">
        <div
          v-for="c in categories"
          :key="c.id"
          class="category-card"
          @click="$router.push(`/category/${c.id}`)"
        >
          <div class="cat-content">
            <span class="cat-count">{{ c.article_count || 0 }}</span>
            <h3 class="cat-name">{{ c.name }}</h3>
            <p class="cat-desc" v-if="c.description">{{ c.description }}</p>
          </div>
          <div class="cat-accent"></div>
        </div>
        <div class="empty-state" v-if="!categories.length">
          <p>暂无分类</p>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCategories } from '@/api'
import MainLayout from '@/layouts/MainLayout.vue'

const categories = ref([])

onMounted(async () => {
  try {
    const data = await getCategories()
    categories.value = Array.isArray(data) ? data : (data.results || [])
  } catch { categories.value = [] }
})
</script>

<style scoped>
.page {
  max-width: var(--content-width);
  margin: 0 auto;
  padding: 80px 24px 80px;
}

.page-header {
  text-align: center;
  margin-bottom: 56px;
}

.page-title {
  font-size: 36px;
  font-weight: 800;
  letter-spacing: -0.03em;
  margin-bottom: 12px;
}

.page-sub {
  font-size: 15px;
  color: var(--text-tertiary);
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.category-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s var(--ease-out);
}

.category-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: transparent;
}

.cat-content {
  padding: 36px 28px;
}

.cat-count {
  display: block;
  font-size: 48px;
  font-weight: 800;
  color: var(--accent);
  line-height: 1;
  margin-bottom: 14px;
  opacity: 0.85;
}

.cat-name {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 8px;
}

.cat-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

.cat-accent {
  height: 3px;
  background: var(--accent-gradient);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s var(--ease-out);
}

.category-card:hover .cat-accent {
  transform: scaleX(1);
}

.empty-state {
  text-align: center;
  color: var(--text-tertiary);
  padding: 80px 0;
  grid-column: 1 / -1;
}

@media (max-width: 640px) {
  .page {
    padding: 60px 16px 60px;
  }

  .categories-grid {
    grid-template-columns: 1fr;
  }
}
</style>