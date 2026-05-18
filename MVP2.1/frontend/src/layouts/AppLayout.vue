<template>
  <div class="app-layout">
    <!-- 左侧导航栏 -->
    <SidebarNav />
    
    <!-- 右侧内容区 -->
    <main class="main-content">
      <!-- 页面标题栏 -->
      <header class="page-header">
        <h1 class="page-title">{{ pageTitle }}</h1>
        <p v-if="pageSubtitle" class="page-subtitle">{{ pageSubtitle }}</p>
      </header>
      
      <!-- 页面内容 -->
      <div class="page-body">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import SidebarNav from '../components/SidebarNav.vue'

const route = useRoute()

// 从路由meta获取页面标题
const pageTitle = computed(() => {
  const titles = {
    'MemoryCorridor': '记忆长廊',
    'IdeaFreeze': '想法定格',
    'HealingSpace': '疗愈空间',
    'PrivateUniverse': '私人宇宙',
  }
  return titles[route.name] || 'MemChain'
})

const pageSubtitle = computed(() => {
  const subtitles = {
    'MemoryCorridor': '用时间轴串联每一段珍贵记忆',
    'IdeaFreeze': '记录当下的想法与感受',
    'HealingSpace': 'AI智能分析，读懂你的情绪',
    'PrivateUniverse': '你的记忆数据可视化仪表盘',
  }
  return subtitles[route.name] || ''
})
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
}

.main-content {
  margin-left: var(--sidebar-width);
  flex: 1;
  min-height: 100vh;
  padding: 24px 32px;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
}

.page-body {
  background: var(--bg-card);
  border-radius: var(--card-radius);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  min-height: calc(100vh - 180px);
}
</style>