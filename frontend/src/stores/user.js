import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    username: '',
    isLoggedIn: false,
    role: '' // 'user' or 'admin'
  }),
  actions: {
    login(username, role) {
      this.username = username
      this.role = role
      this.isLoggedIn = true
    },
    logout() {
      this.username = ''
      this.role = ''
      this.isLoggedIn = false
    }
  },
  persist: true
})
