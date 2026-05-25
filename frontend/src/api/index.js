import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || '/api'

const request = axios.create({
  baseURL: API_BASE,
  timeout: 10000
})

request.interceptors.response.use(
  response => response.data,
  error => Promise.reject(error)
)

export const getArticles = (params) => request.get('/articles/', { params })
export const getArticle = (id) => request.get(`/articles/${id}/`)
export const getHotArticles = () => request.get('/articles/hot/')
export const getRecentArticles = () => request.get('/articles/recent/')

export const getCategories = () => request.get('/categories/')
export const getTags = () => request.get('/tags/')

export const getComments = (params) => request.get('/comments/', { params })
export const createComment = (data) => request.post('/comments/', data)

export const getFriendlyLinks = () => request.get('/friendly-links/')
export const getPersonalLinks = () => request.get('/personal-links/')

export const getSiteSettings = () => request.get('/site-settings/')
export const getStatistics = () => request.get('/statistics/')

export default request