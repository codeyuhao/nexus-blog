import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomePage.vue'),
    meta: { title: 'Home' }
  },
  {
    path: '/article/:id',
    name: 'Article',
    component: () => import('@/views/ArticlePage.vue'),
    meta: { title: 'Article' }
  },
  {
    path: '/category',
    name: 'Categories',
    component: () => import('@/views/CategoriesPage.vue'),
    meta: { title: 'Categories' }
  },
  {
    path: '/category/:id',
    name: 'CategoryArticles',
    component: () => import('@/views/CategoryArticles.vue'),
    meta: { title: 'Category' }
  },
  {
    path: '/tag',
    name: 'Tags',
    component: () => import('@/views/TagsPage.vue'),
    meta: { title: 'Tags' }
  },
  {
    path: '/tag/:id',
    name: 'TagArticles',
    component: () => import('@/views/TagArticles.vue'),
    meta: { title: 'Tag' }
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import('@/views/SearchPage.vue'),
    meta: { title: 'Search' }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/AboutPage.vue'),
    meta: { title: 'About' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} · Nexus` : 'Nexus · Blog'
  next()
})

export default router