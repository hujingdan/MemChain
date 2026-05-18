<template>
  <aside class="sidebar">
    <!-- Logo区域 -->
    <div class="logo-area">
      <img src="/logo.png" alt="MemChain" class="logo-img" />
      <span class="logo-text">MemChain</span>
    </div>

    <!-- 导航菜单 -->
    <nav class="nav-menu">
      <router-link
        v-for="item in navItems"
        :key="item.key"
        :to="item.path"
        class="nav-item"
        :class="{ active: currentNav === item.key }"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        <span class="nav-label">{{ item.label }}</span>
      </router-link>
    </nav>

    <!-- 底部用户信息 -->
    <div class="user-area">
      <div class="user-info">
        <div class="user-avatar">{{ userInitial }}</div>
        <span class="user-name">{{ userStore.displayName }}</span>
      </div>
      <div class="user-actions">
        <button class="icon-btn" title="设置">⚙</button>
        <button class="icon-btn" title="退出" @click="userStore.logout">⎋</button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '../stores/user.js'

const route = useRoute()
const userStore = useUserStore()

// 导航配置（与router/index.js对应）
const navItems = [
  { key: 'corridor', label: '近期展览', icon: '\u{1F5BC}', path: '/corridor' },
  { key: 'editor',   label: '即刻记录', icon: '\u{270D}',  path: '/editor' },
  { key: 'healing',  label: '疗愈空间', icon: '\u{1F3B5}', path: '/healing' },
  { key: 'universe', label: '主题回顾', icon: '\u{1F30C}', path: '/universe' },
//  { key: 'messages', label: '消息邮箱', icon: '\u{2709}',  path: '/messages' },
]

// 当前激活的导航项
const currentNav = computed(() => route.meta.navKey || 'corridor')

// 用户名字首字母（用于头像占位）
const userInitial = computed(() => {
  const name = userStore.displayName
  return name ? name.charAt(0).toUpperCase() : '?'
})
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: var(--sidebar-width);
  background: linear-gradient(180deg, #E88B7C 0%, #D47366 100%);
  display: flex;
  flex-direction: column;
  padding: 24px 16px 16px;
  z-index: 50;
  box-shadow: 4px 0 20px rgba(0,0,0,0.08);
}

/* Logo区域 */
.logo-area {
  display: flex;
  align-items: center;
  gap: 0.1px;
  margin-bottom: 32px;
  padding-left: -3px;
  margin-left: -12px;    /* 🔥 关键：负 margin 让Logo单独左移！数值自己调 */
}

.logo-img {
  width: 75px;
  height: 60px;
  object-fit: contain;
  filter: brightness(0) invert(1);  /* 白色Logo */
}

.logo-text {
  font-size: 28px;
  font-weight: 700;
  color: white;
  letter-spacing: 0.5px;
}

/* 导航菜单 */
.nav-menu {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: var(--btn-radius);
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  transition: all var(--transition-fast);
  cursor: pointer;
}

.nav-item:hover {
  background: rgba(255,255,255,0.12);
  color: white;
}

.nav-item.active {
  background: rgba(255,255,255,0.2);
  color: white;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.nav-icon {
  font-size: 20px;
  width: 24px;
  text-align: center;
}

.nav-label {
  font-size: 15px;
}

/* 用户信息区域 */
.user-area {
  border-top: 1px solid rgba(255,255,255,0.15);
  padding-top: 16px;
  margin-top: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  padding-left: 8px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255,255,255,0.25);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
}

.user-name {
  color: rgba(255,255,255,0.9);
  font-size: 14px;
  font-weight: 500;
}

.user-actions {
  display: flex;
  gap: 8px;
  padding-left: 8px;
}

.icon-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.8);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.icon-btn:hover {
  background: rgba(255,255,255,0.2);
  color: white;
}
</style>