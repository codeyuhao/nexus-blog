<template>
  <MainLayout>
    <div class="article-page" v-if="article.title">
      <header class="article-header">
        <div class="article-header-inner">
          <button class="back-link" @click="$router.back()">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
            返回
          </button>
          <div class="article-cat" v-if="article.category">
            <span class="cat-indicator"></span>
            {{ article.category.name }}
          </div>
          <h1 class="article-title">{{ article.title }}</h1>
          <div class="article-meta">
            <span class="meta-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
              {{ formatDate(article.created_at) }}
            </span>
            <span class="meta-sep"></span>
            <span class="meta-item">{{ article.views || 0 }} 次阅读</span>
            <span class="meta-sep"></span>
            <span class="meta-item">约 {{ readTime }} 分钟</span>
          </div>
          <div class="article-tags" v-if="article.tags?.length">
            <router-link v-for="t in article.tags" :key="t.id" :to="`/tag/${t.id}`" class="tag-link">{{ t.name }}</router-link>
          </div>
        </div>
      </header>
      <article class="article-content">
        <div class="markdown-body" v-html="rendered"></div>
      </article>
      <section class="comments-section">
        <div class="comments-inner">
          <h3 class="comments-title">
            评论
            <span class="comments-count" v-if="comments.length">{{ comments.length }}</span>
          </h3>
          <div class="comment-form">
            <div class="form-fields">
              <input
                v-model="form.author_name"
                placeholder="昵称 *"
                class="form-input"
                :class="{ error: formErrors.name }"
              />
              <input
                v-model="form.author_email"
                placeholder="邮箱（选填）"
                class="form-input"
              />
            </div>
            <textarea
              v-model="form.content"
              placeholder="写下你的想法..."
              rows="4"
              class="form-textarea"
              :class="{ error: formErrors.content }"
            ></textarea>
            <button class="form-submit" @click="submitComment" :disabled="submitting">
              {{ submitting ? '发送中...' : '发表评论' }}
            </button>
            <p class="form-hint" v-if="submitSuccess">评论已提交</p>
            <p class="form-hint error" v-if="submitError">{{ submitError }}</p>
          </div>
          <div class="comments-list" v-if="comments.length">
            <div v-for="c in comments" :key="c.id" class="comment-card">
              <div class="comment-avatar">{{ c.author_name?.charAt(0)?.toUpperCase() || '?' }}</div>
              <div class="comment-main">
                <div class="comment-head">
                  <span class="comment-name">{{ c.author_name }}</span>
                  <span class="comment-time">{{ formatDate(c.created_at) }}</span>
                </div>
                <p class="comment-text">{{ c.content }}</p>
              </div>
            </div>
          </div>
          <p class="no-comments" v-else>暂无评论，来做第一个评论的人吧。</p>
        </div>
      </section>
    </div>
    <div class="loading-state" v-else-if="loading">
      <div class="loading-spinner"></div>
    </div>
    <div class="error-state" v-else>
      <p>文章不存在或已被删除</p>
      <router-link to="/" class="error-link">返回首页</router-link>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from 'vue'
import { useRoute } from 'vue-router'
import { getArticle, getComments, createComment } from '@/api'
import { renderMarkdown } from '@/utils/markdown'
import MainLayout from '@/layouts/MainLayout.vue'

const route = useRoute()
const article = ref({})
const comments = ref([])
const loading = ref(true)
const form = reactive({ author_name: '', author_email: '', content: '' })
const formErrors = reactive({ name: false, content: false })
const submitting = ref(false)
const submitSuccess = ref(false)
const submitError = ref('')

const rendered = computed(() => article.value.content_html || renderMarkdown(article.value.content || ''))
const readTime = computed(() => Math.max(1, Math.ceil((article.value.content?.length || 0) / 800)))

const formatDate = (d) => {
  if (!d) return ''
  const date = new Date(d)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

const fetchComments = async () => {
  try {
    const data = await getComments({ article: route.params.id })
    comments.value = Array.isArray(data) ? data : (data.results || [])
  } catch { comments.value = [] }
}

const submitComment = async () => {
  formErrors.name = false
  formErrors.content = false
  submitError.value = ''
  submitSuccess.value = false

  if (!form.author_name.trim()) { formErrors.name = true; return }
  if (!form.content.trim()) { formErrors.content = true; return }

  submitting.value = true
  try {
    await createComment({ ...form, article: route.params.id })
    form.author_name = ''
    form.author_email = ''
    form.content = ''
    submitSuccess.value = true
    setTimeout(() => submitSuccess.value = false, 3000)
    fetchComments()
  } catch (e) {
    submitError.value = '评论提交失败，请稍后重试'
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  try {
    article.value = await getArticle(route.params.id)
  } catch { article.value = {} }
  finally { loading.value = false }
  fetchComments()
})
</script>

<style scoped>
.article-page {
  min-height: 100vh;
}

.article-header {
  padding: 80px 24px 48px;
  background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
}

.article-header-inner {
  max-width: var(--read-width);
  margin: 0 auto;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  margin-bottom: 24px;
  padding: 6px 12px;
  border-radius: 8px;
  transition: all 0.2s;
}

.back-link:hover {
  background: var(--bg-card);
  color: var(--accent);
}

.article-cat {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--accent);
  margin-bottom: 16px;
}

.cat-indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
}

.article-title {
  font-size: clamp(26px, 4vw, 40px);
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -0.025em;
  margin-bottom: 20px;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 14px;
  color: var(--text-tertiary);
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.meta-sep {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: var(--text-tertiary);
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-link {
  padding: 5px 14px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  transition: all 0.2s;
}

.tag-link:hover {
  color: var(--accent);
  border-color: var(--accent);
  background: var(--accent-soft);
}

.article-content {
  max-width: var(--read-width);
  margin: 0 auto;
  padding: 48px 24px 20px;
}

.comments-section {
  border-top: 1px solid var(--border-color);
  padding: 64px 24px 80px;
  background: var(--bg-secondary);
  margin-top: 60px;
}

.comments-inner {
  max-width: var(--read-width);
  margin: 0 auto;
}

.comments-title {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 32px;
}

.comments-count {
  font-weight: 400;
  color: var(--text-tertiary);
  font-size: 16px;
  margin-left: 8px;
}

.comment-form {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 24px;
  margin-bottom: 40px;
}

.form-fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 12px;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 12px 16px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-family: var(--font-sans);
  color: var(--text-primary);
  outline: none;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  border-color: var(--accent);
}

.form-input.error,
.form-textarea.error {
  border-color: #ef4444;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
  margin-bottom: 16px;
}

.form-submit {
  padding: 12px 28px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  font-family: var(--font-sans);
  cursor: pointer;
  transition: all 0.2s;
}

.form-submit:hover:not(:disabled) {
  background: var(--accent-hover);
}

.form-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-hint {
  margin-top: 10px;
  font-size: 13px;
  color: #22c55e;
}

.form-hint.error {
  color: #ef4444;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-card {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
}

.comment-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: var(--accent-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
}

.comment-main {
  flex: 1;
  min-width: 0;
}

.comment-head {
  display: flex;
  gap: 12px;
  align-items: baseline;
  margin-bottom: 8px;
}

.comment-name {
  font-weight: 600;
  font-size: 14px;
}

.comment-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

.comment-text {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
}

.no-comments {
  text-align: center;
  color: var(--text-tertiary);
  padding: 40px 0;
  font-size: 15px;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  gap: 16px;
}

.error-state p {
  font-size: 16px;
  color: var(--text-secondary);
}

.error-link {
  color: var(--accent);
  font-weight: 600;
}

@media (max-width: 640px) {
  .article-header {
    padding: 70px 16px 36px;
  }

  .article-content {
    padding: 32px 16px 16px;
  }

  .comments-section {
    padding: 48px 16px 60px;
  }

  .form-fields {
    grid-template-columns: 1fr;
  }
}
</style>