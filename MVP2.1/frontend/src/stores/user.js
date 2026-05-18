/**
 * stores/user.js - 用户全局状态（Pinia）
 * 存储当前登录用户信息，所有组件共享。
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // ========== State ==========
  // 当前用户信息（Phase 2接入真实数据）
  const user = ref({
    id: 'demo_user',
    username: 'demo',
    nickname: '记忆收藏家',
    avatar: null,
    isLoggedIn: true,  // TODO: Phase 2改为从localStorage读token判断
  })
  
  // ========== Getters ==========
  const isLoggedIn = computed(() => user.value?.isLoggedIn ?? false)
  const displayName = computed(() => user.value?.nickname || user.value?.username || '访客')
  
  // ========== Actions ==========
  function setUser(userData) {
    user.value = { ...user.value, ...userData }
  }
  
  function logout() {
    user.value = { isLoggedIn: false }
    localStorage.removeItem('token')
    window.location.href = '/login'
  }
  
  return {
    user,
    isLoggedIn,
    displayName,
    setUser,
    logout,
  }
})