import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: number
  email: string
  username: string
  full_name?: string
}

interface Message {
  id?: number
  role: 'user' | 'assistant' | 'system'
  content: string
  created_at?: string
}

interface Conversation {
  id: number
  title: string
  messages: Message[]
  created_at: string
  updated_at: string
}

interface AppState {
  user: User | null
  setUser: (user: User | null) => void
  
  currentConversation: Conversation | null
  setCurrentConversation: (conversation: Conversation | null) => void
  
  conversations: Conversation[]
  setConversations: (conversations: Conversation[]) => void
  
  addMessage: (message: Message) => void
  
  isLoading: boolean
  setIsLoading: (loading: boolean) => void
  
  sidebarOpen: boolean
  setSidebarOpen: (open: boolean) => void
  
  logout: () => void
}

export const useStore = create<AppState>()(persist(
  (set) => ({
    user: null,
    setUser: (user) => set({ user }),
    
    currentConversation: null,
    setCurrentConversation: (conversation) => set({ currentConversation: conversation }),
    
    conversations: [],
    setConversations: (conversations) => set({ conversations }),
    
    addMessage: (message) => set((state) => ({
      currentConversation: state.currentConversation
        ? {
            ...state.currentConversation,
            messages: [...state.currentConversation.messages, message],
          }
        : null,
    })),
    
    isLoading: false,
    setIsLoading: (loading) => set({ isLoading: loading }),
    
    sidebarOpen: true,
    setSidebarOpen: (open) => set({ sidebarOpen: open }),
    
    logout: () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      set({ user: null, currentConversation: null, conversations: [] })
    },
  }),
  {
    name: 'nexus-storage',
    partialize: (state) => ({ user: state.user, sidebarOpen: state.sidebarOpen }),
  }
))