<template>
  <div class="memory-corridor">
    <!-- 情绪折线图 -->
    <EmotionChart />
    
    <!-- 记忆卡片列表标题 -->
    <div class="section-header">
      <h2 class="section-title">我的记忆素材</h2>
      <button class="refresh-btn" @click="fetchRecent" :disabled="loading">
        {{ loading ? '加载中...' : '刷新' }}
      </button>
    </div>
    
    <!-- 记忆卡片瀑布流 -->
    <div v-if="loading && items.length === 0" class="loading-state">正在加载记忆...</div>
    <div v-else-if="items.length === 0" class="empty-state">
      <div class="empty-icon">\u{1F4C1}</div>
      <p>还没有上传任何记忆素材</p>
      <p class="empty-hint">点击右下角按钮，开始记录你的第一段记忆</p>
    </div>
    <div v-else class="memory-grid">
      <MemoryCard
        v-for="item in items"
        :key="item.id"
        :item="item"
        @click="openDetail"
      />
    </div>
    
    <!-- 浮动FAB按钮 -->
    <router-link to="/editor" class="fab-btn" title="记录新记忆">
      <span class="fab-icon">+</span>
    </router-link>
    
    <!-- AI详情弹窗（复用现有弹窗逻辑） -->
    <div v-if="selectedItem" class="modal-overlay" @click="selectedItem = null">
      <div class="modal-content" @click.stop>
        <h3>AI 分析报告</h3>
        <div v-if="selectedItem.properties?.ai_tag">
          <p class="ai-tag-large">{{ selectedItem.properties.ai_tag }}</p>
          <div v-if="selectedItem.properties.dominant_colors" class="color-palette">
            <div
              v-for="(c, i) in selectedItem.properties.dominant_colors"
              :key="i"
              class="color-block"
              :style="{backgroundColor: `rgb(${c[0]},${c[1]},${c[2]})`}"
            />
          </div>
          <div v-if="selectedItem.properties.brightness !== undefined" class="brightness-bar">
            <p>亮度：{{ selectedItem.properties.brightness }} / 255</p>
            <div class="bar-track">
              <div class="bar-fill" :style="{width: (selectedItem.properties.brightness/255*100)+'%'}" />
            </div>
          </div>
        </div>
        <div v-else class="no-ai">
          <p>暂无AI分析数据</p>
        </div>
        <button class="close-btn" @click="selectedItem = null">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import EmotionChart from '../components/EmotionChart.vue'
import MemoryCard from '../components/MemoryCard.vue'
import { API_BASE } from '../shared/constants.js'

const items = ref([])
const loading = ref(false)
const selectedItem = ref(null)

async function fetchRecent() {
  loading.value = true
  try {
    const response = await fetch(`${API_BASE}/timeline/entries/recent?limit=50`)
    const result = await response.json()
    if (result.success) {
      items.value = result.data.items || []
    }
  } catch (err) {
    console.error('获取记忆列表失败:', err)
  } finally {
    loading.value = false
  }
}

function openDetail(item) {
  selectedItem.value = item
}

onMounted(() => {
  fetchRecent()
})
</script>

<style scoped>
.memory-corridor {
  position: relative;
  padding-bottom: 80px;  /* 给FAB按钮留空间 */
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 24px 0 16px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.refresh-btn {
  padding: 8px 18px;
  border: 1px solid var(--border);
  background: var(--bg-card);
  color: var(--primary);
  border-radius: var(--btn-radius);
  cursor: pointer;
  font-size: 13px;
  transition: all var(--transition-fast);
}

.refresh-btn:hover {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}

.memory-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-tertiary);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.4;
}

.empty-hint {
  font-size: 13px;
  margin-top: 8px;
  color: var(--text-secondary);
}

/* FAB按钮 */
.fab-btn {
  position: fixed;
  right: 40px;
  bottom: 40px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  box-shadow: var(--shadow-lg);
  transition: all var(--transition-normal);
  z-index: 40;
}

.fab-btn:hover {
  transform: scale(1.1) ;
  box-shadow: 0 10px 30px rgba(232, 139, 124, 0.4);
}

.fab-icon {
  font-size: 40px;
  font-weight: 500;
  line-height: 1; /* 消除字体默认行高，确保垂直居中 */
  transform: translateY(-2.6px); /* 🔴 微调1px，解决加号视觉偏上的通病 */
}

/* 弹窗样式（与之前一致，简化版） */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-content {
  background: var(--bg-card);
  border-radius: var(--card-radius);
  padding: 28px;
  max-width: 380px;
  width: 90%;
}

.modal-content h3 {
  text-align: center;
  margin-bottom: 20px;
  color: var(--text-primary);
}

.ai-tag-large {
  font-size: 18px;
  color: var(--primary);
  font-weight: 600;
  text-align: center;
  margin-bottom: 20px;
}

.color-palette {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-bottom: 20px;
}

.color-block {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.brightness-bar {
  margin-bottom: 20px;
}

.bar-track {
  height: 8px;
  background: var(--border-light);
  border-radius: 4px;
  overflow: hidden;
  margin-top: 8px;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #333, #ddd, #fff);
  border-radius: 4px;
  transition: width 0.8s ease;
}

.no-ai {
  text-align: center;
  color: var(--text-tertiary);
  padding: 20px;
}

.close-btn {
  width: 100%;
  padding: 10px;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: var(--btn-radius);
  cursor: pointer;
  margin-top: 16px;
}

.close-btn:hover {
  background: var(--primary-dark);
}
</style>