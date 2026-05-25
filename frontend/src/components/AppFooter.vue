<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <div class="footer-grid">
        <div class="footer-brand">
          <span class="footer-logo">Nexus</span>
          <p class="footer-tagline">记录思考，分享创造。</p>
        </div>
        <div class="footer-links-group">
          <h4 class="footer-heading">导航</h4>
          <router-link to="/">首页</router-link>
          <router-link to="/category">分类</router-link>
          <router-link to="/tag">标签</router-link>
          <router-link to="/about">关于</router-link>
        </div>
        <div class="footer-links-group">
          <h4 class="footer-heading">社交</h4>
          <a href="#" target="_blank">GitHub</a>
          <a href="#" target="_blank">Twitter</a>
          <a href="#" target="_blank">RSS</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; {{ year }} Nexus Blog. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear()
</script>

<style scoped>
.app-footer {
  background: var(--bg-card);
  border-top: 1px solid var(--border-color);
  margin-top: 100px;
}

.footer-inner {
  max-width: var(--content-width);
  margin: 0 auto;
  padding: 64px 24px 32px;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr;
  gap: 48px;
  margin-bottom: 48px;
}

.footer-brand {
  max-width: 280px;
}

.footer-logo {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -0.03em;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.footer-tagline {
  margin-top: 12px;
  font-size: 14px;
  color: var(--text-tertiary);
  line-height: 1.6;
}

.footer-links-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.footer-heading {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-tertiary);
  margin-bottom: 4px;
}

.footer-links-group a {
  font-size: 14px;
  color: var(--text-secondary);
  transition: color 0.2s;
}

.footer-links-group a:hover {
  color: var(--accent);
}

.footer-bottom {
  padding-top: 24px;
  border-top: 1px solid var(--border-light);
}

.footer-bottom p {
  font-size: 13px;
  color: var(--text-tertiary);
}

@media (max-width: 640px) {
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 32px;
    margin-bottom: 32px;
  }

  .footer-inner {
    padding: 48px 20px 24px;
  }
}
</style>