<template>
  <div class="memory-card" @click="$emit('click', item)">
    <!-- 媒体预览区 -->
    <div class="media-preview">
      <img
        v-if="item.type === 'images'"
        :src="`${API_BASE}/upload/preview/${item.id}`"
        alt="preview"
        loading="lazy"
        class="preview-img"
      />
      <div v-else class="file-type-icon">{{ getTypeIcon(item.type) }}</div>
    </div>
    
    <!-- 信息区 -->
    <div class="card-info">
      <p class="card-title" :title="item.title">{{ truncate(item.title, 22) }}</p>
      <p class="card-meta">{{ formatSize(item.size) }} · {{ formatDate(item.created_at) }}</p>
      
      <!-- AI标签 -->
      <p v-if="item.properties?.ai_tag" class="ai-tag">
        AI: {{ item.properties.ai_tag }}
      </p>
      
      <!-- 情绪标签（如果有） -->
      <p v-if="item.properties?.emotion_label" class="emotion-tag">
        {{ getEmotionIcon(item.properties.emotion_label) }} {{ getEmotionLabel(item.properties.emotion_label) }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { API_BASE, EMOTION_MAP } from '../shared/constants.js'

defineProps(['item'])
defineEmits(['click'])

function getTypeIcon(type) {
  const icons = { images: '\u{1F5BC}', audio: '\u{1F3B5}', text: '\u{1F4C4}', documents: '\u{1F4C4}' }
  return icons[type] || '\u{1F4C1}'
}

function getEmotionIcon(key) {
  return EMOTION_MAP[key]?.icon || ''
}

function getEmotionLabel(key) {
  return EMOTION_MAP[key]?.label || key
}

function truncate(str, len) {
  if (!str) return ''
  return str.length > len ? str.slice(0, len) + '...' : str
}

function formatSize(bytes) {
  if (!bytes) return '0 B'
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1024 / 1024).toFixed(1) + ' MB'
}

function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}
</script>

<style scoped>
.memory-card {
  background: var(--bg-card);
  border-radius: var(--card-radius);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-normal);
  cursor: pointer;
}

.memory-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.media-preview {
  height: 160px;
  background: linear-gradient(135deg, #FFF0ED 0%, #FFE8E0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.memory-card:hover .preview-img {
  transform: scale(1.05);
}

.file-type-icon {
  font-size: 48px;
  opacity: 0.6;
}

.card-info {
  padding: 14px 16px;
}

.card-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-meta {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-bottom: 8px;
}

.ai-tag {
  display: inline-block;
  font-size: 11px;
  color: var(--tag-ai-text);
  background: var(--tag-ai-bg);
  padding: 3px 8px;
  border-radius: 10px;
  margin-bottom: 4px;
}

.emotion-tag {
  display: inline-block;
  font-size: 11px;
  color: var(--primary-dark);
  background: var(--tag-bg);
  padding: 3px 8px;
  border-radius: 10px;
}
</style>