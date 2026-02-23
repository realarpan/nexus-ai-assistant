import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Req interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Resp. interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_URL}/api/v1/auth/refresh`, {
            refresh_token: refreshToken,
          })
          
          const { access_token } = response.data
          localStorage.setItem('access_token', access_token)
          
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return api(originalRequest)
        } catch (err) {
          localStorage.clear()
          window.location.href = '/login'
          return Promise.reject(err)
        }
      }
    }

    return Promise.reject(error)
  }
)

export default api

// API functions
export const authAPI = {
  register: (data: { email: string; username: string; password: string; full_name?: string }) =>
    api.post('/auth/register', data),
  
  login: (username: string, password: string) => {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    return api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  
  getMe: () => api.get('/auth/me'),
}

export const chatAPI = {
  sendMessage: (data: { message: string; conversation_id?: number }) =>
    api.post('/chat/message', data),
  
  getConversations: () => api.get('/chat/conversations'),
  
  getConversation: (id: number) => api.get(`/chat/conversations/${id}`),
  
  deleteConversation: (id: number) => api.delete(`/chat/conversations/${id}`),
}

export const documentsAPI = {
  upload: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  
  getAll: () => api.get('/documents'),
}