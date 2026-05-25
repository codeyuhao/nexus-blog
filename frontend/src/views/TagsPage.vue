<template>
  <MainLayout>
    <div class="page">
      <header class="page-header">
        <h1 class="page-title">标签</h1>
        <p class="page-sub">按标签探索文章主题</p>
      </header>
      <div class="tags-wrapper">
        <router-link
          v-for="t in tags"
          :key="t.id"
          :to="`/tag/${t.id}`"
          class="tag-item"
        >
          {{ t.name }}
        </router-link>
        <p class="empty-state" v-if="!tags.length">暂无标签</p>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTags } from '@/api'
import MainLayout from '@/layouts/MainLayout.vue'

const tags = ref([])

onMounted(async () => {
  try {
    const data = await getTags()
    tags.value = Array.isArray(data) ? data : (data.results || [])
  } catch { tags.value = [] }
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

.tags-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
  max-width: 680px;
  margin: 0 auto;
}

.tag-item {
  padding: 10px 22px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 24px;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-secondary);
  transition: all 0.25s var(--ease-out);
}

.tag-item:hover {
  color: var(--accent);
  border-color: var(--accent);
  background: var(--accent-soft);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.empty-state {
  text-align: center;
  color: var(--text-tertiary);
  padding: 80px 0;
  width: 100%;
}
</style>