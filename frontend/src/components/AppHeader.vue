<template>
  <header class="app-header" :class="{ 'is-scrolled': isScrolled }">
    <div class="header-inner">
      <router-link to="/" class="header-brand">
        <div class="brand-mark">
          <svg width="22" height="22" viewBox="0 0 32 32" fill="none">
            <circle cx="16" cy="16" r="14" stroke="url(#brand-gradient)" stroke-width="3"/>
            <circle cx="16" cy="16" r="5" fill="url(#brand-gradient)"/>
            <defs>
              <linearGradient id="brand-gradient" x1="0" y1="0" x2="32" y2="32">
                <stop offset="0%" stop-color="#6366f1"/>
                <stop offset="100%" stop-color="#a855f7"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <span class="brand-text">Nexus</span>
      </router-link>

      <nav class="header-nav">
        <router-link to="/" class="nav-item" exact-active-class="is-active">首页</router-link>
        <router-link to="/category" class="nav-item" active-class="is-active">分类</router-link>
        <router-link to="/tag" class="nav-item" active-class="is-active">标签</router-link>
        <router-link to="/about" class="nav-item" active-class="is-active">关于</router-link>
      </nav>

      <div class="header-actions">
        <button class="search-trigger" @click="showSearch = true" aria-label="搜索">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
        </button>
        <button class="mobile-menu-btn" @click="mobileOpen = !mobileOpen" aria-label="菜单">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <line x1="3" y1="6" x2="21" y2="6" v-if="!mobileOpen"/>
            <line x1="3" y1="12" x2="21" y2="12" v-if="!mobileOpen"/>
            <line x1="3" y1="18" x2="21" y2="18" v-if="!mobileOpen"/>
            <line x1="18" y1="6" x2="6" y2="18" v-if="mobileOpen"/>
            <line x1="6" y1="6" x2="18" y2="18" v-if="mobileOpen"/>
          </svg>
        </button>
      </div>
    </div>

    <div class="mobile-nav" v-if="mobileOpen">
      <router-link to="/" class="mobile-nav-item" @click="mobileOpen = false">首页</router-link>
      <router-link to="/category" class="mobile-nav-item" @click="mobileOpen = false">分类</router-link>
      <router-link to="/tag" class="mobile-nav-item" @click="mobileOpen = false">标签</router-link>
      <router-link to="/about" class="mobile-nav-item" @click="mobileOpen = false">关于</router-link>
    </div>

    <div class="search-overlay" v-if="showSearch" @click.self="showSearch = false">
      <div class="search-dialog">
        <div class="search-input-wrap">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--text-tertiary)" stroke-width="2" stroke-linecap="round">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input
            ref="searchInput"
            v-model="searchKeyword"
            class="search-input"
            placeholder="搜索文章..."
            @keyup.enter="doSearch"
          />
          <button class="search-close" @click="showSearch = false">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isScrolled = ref(false)
const mobileOpen = ref(false)
const showSearch = ref(false)
const searchKeyword = ref('')
const searchInput = ref(null)

const onScroll = () => {
  isScrolled.value = window.scrollY > 20
}

const doSearch = () => {
  const kw = searchKeyword.value.trim()
  if (!kw) return
  showSearch.value = false
  searchKeyword.value = ''
  router.push(`/search?keyword=${encodeURIComponent(kw)}`)
}

const openSearch = async () => {
  showSearch.value = true
  await nextTick()
  searchInput.value?.focus()
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  transition: all 0.3s var(--ease-out);
}

.app-header.is-scrolled {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow-xs);
}

.header-inner {
  max-width: var(--content-width);
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.brand-mark {
  display: flex;
}

.brand-text {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.03em;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-item {
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  border-radius: 8px;
  transition: all 0.2s;
}

.nav-item:hover {
  color: var(--text-primary);
  background: var(--bg-secondary);
}

.nav-item.is-active {
  color: var(--accent);
  background: var(--accent-soft);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-trigger {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border: none;
  background: var(--bg-secondary);
  border-radius: 10px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.search-trigger:hover {
  background: var(--accent-soft);
  color: var(--accent);
}

.mobile-menu-btn {
  display: none;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border: none;
  background: var(--bg-secondary);
  border-radius: 10px;
  color: var(--text-secondary);
  cursor: pointer;
}

.mobile-nav {
  display: none;
  padding: 8px 24px 16px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-color);
}

.mobile-nav-item {
  display: block;
  padding: 12px 16px;
  font-size: 15px;
  font-weight: 500;
  color: var(--text-secondary);
  border-radius: 8px;
  transition: all 0.2s;
}

.mobile-nav-item:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.search-overlay {
  position: fixed;
  inset: 0;
  z-index: 1100;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 25vh;
}

.search-dialog {
  width: 100%;
  max-width: 560px;
  margin: 0 24px;
}

.search-input-wrap {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 20px;
  background: var(--bg-card);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  transition: border-color 0.2s;
}

.search-input-wrap:focus-within {
  border-color: var(--accent);
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
  font-family: var(--font-sans);
  color: var(--text-primary);
  background: transparent;
}

.search-input::placeholder {
  color: var(--text-tertiary);
}

.search-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: var(--bg-secondary);
  border-radius: 8px;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all 0.2s;
}

.search-close:hover {
  background: #fee2e2;
  color: #ef4444;
}

@media (max-width: 768px) {
  .header-nav {
    display: none;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .mobile-nav {
    display: block;
  }
}
</style>