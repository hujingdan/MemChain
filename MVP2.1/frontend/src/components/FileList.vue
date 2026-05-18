<template>
  <div class="file-list-section">
    <div class="list-header">
      <h2>我的记忆素材</h2>
      <button class="refresh-btn" @click="fetchFiles" :disabled="loading">
        {{ loading ? '加载中...' : '刷新' }}
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">正在加载...</div>

    <!-- 空状态 -->
    <div v-else-if="files.length === 0" class="empty">
      <p>还没有上传任何素材</p>
      <p class="empty-hint">上传一张照片、一段录音或一篇笔记，开始记录你的时光</p>
    </div>

    <!-- 文件列表 -->
    <div v-else class="file-grid">
      <div v-for="file in files" :key="file.id" class="file-card" @click="openDetail(file)">
        <!-- 图片预览 -->
        <div class="file-preview">
          <img
            v-if="file.type === 'images'"
            :src="`${API_BASE}/upload/preview/${file.id}`"
            alt="preview"
            loading="lazy"
          />
          <div v-else class="file-icon">{{ getFileIcon(file.type) }}</div>
        </div>

        <!-- 文件信息 -->
        <div class="file-info">
          <p class="file-name" :title="file.name">{{ truncate(file.name, 20) }}</p>
          <p class="file-meta">
            {{ formatSize(file.size) }} · {{ formatDate(file.created_at) }}
          </p>
          <!-- AI标签 -->
          <p v-if="file.properties?.ai_tag" class="ai-tag">
            AI: {{ file.properties.ai_tag }}
          </p>
        </div>

        <!-- 操作按钮 -->
        <div class="file-actions">
          <a
            :href="`${API_BASE}/upload/preview/${file.id}`"
            target="_blank"
            class="action-btn view"
            @click.stop
            title="查看"
          >
            查看
          </a>
          <button class="action-btn delete" @click.stop="deleteFile(file.id)" title="删除">
            删除
          </button>
        </div>
      </div>
    </div>
    <!-- ========== AI分析详情弹窗 ========== -->
    <div
      v-if="selectedFile"
      class="modal-overlay"
      @click="closeDetail"
    >
      <div class="modal-content" @click.stop>
        <h3>AI 分析报告</h3>

        <div v-if="selectedFile.properties?.ai_tag" class="ai-result">
          <!-- AI标签 -->
          <p class="ai-tag-large">{{ selectedFile.properties.ai_tag }}</p>

          <!-- 主色调 -->
          <div
            v-if="selectedFile.properties.dominant_colors?.length"
            class="color-section"
          >
            <p>主色调：</p>
            <div class="color-palette">
              <div
                v-for="(color, idx) in selectedFile.properties.dominant_colors"
                :key="idx"
                class="color-block"
                :style="{
                  backgroundColor: `rgb(${color[0]},${color[1]},${color[2]})`
                }"
                :title="`RGB(${color[0]}, ${color[1]}, ${color[2]})`"
              ></div>
            </div>
          </div>

          <!-- 亮度条 -->
          <div
            v-if="selectedFile.properties.brightness !== undefined"
            class="brightness-bar"
          >
            <p>亮度：{{ selectedFile.properties.brightness }} / 255</p>
            <div class="bar-track">
              <div
                class="bar-fill"
                :style="{
                  width: (selectedFile.properties.brightness / 255 * 100) + '%'
                }"
              ></div>
            </div>
            <p class="brightness-level">
              {{ selectedFile.properties.brightness_level }}
            </p>
          </div>

          <!-- 尺寸 -->
          <p v-if="selectedFile.properties?.width" class="dimension">
            尺寸：{{ selectedFile.properties.width }} x {{ selectedFile.properties.height }} px
          </p>
        </div>

        <!-- 无AI数据 -->
        <div v-else class="no-ai-data">
          <p>暂无AI分析数据</p>
          <p class="no-ai-hint">该文件上传时可能未完成AI分析</p>
        </div>

        <button class="close-btn" @click="closeDetail">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const files = ref([])
const loading = ref(false)
const selectedFile = ref(null)  // 当前选中的文件（弹窗显示）
const API_BASE = 'http://localhost:8000'

onMounted(() => {
  fetchFiles()
})

async function fetchFiles() {
  loading.value = true
  try {
    const response = await fetch(`${API_BASE}/upload/files?limit=100`)
    const result = await response.json()
    if (response.ok) {
      files.value = result.files || []
    }
  } catch (err) {
    console.error('获取文件列表失败:', err)
  } finally {
    loading.value = false
  }
}

async function deleteFile(fileId) {
  if (!confirm('确定要删除这个素材吗？')) return
  try {
    const response = await fetch(`${API_BASE}/upload/files/${fileId}`, {
      method: 'DELETE'
    })
    if (response.ok) {
      files.value = files.value.filter(f => f.id !== fileId)
      // 如果删除的是当前弹窗中的文件，关闭弹窗
      if (selectedFile.value?.id === fileId) {
        selectedFile.value = null
      }
    }
  } catch (err) {
    alert('删除失败')
  }
}

// 打开详情弹窗
function openDetail(file) {
  selectedFile.value = file
}

// 关闭详情弹窗
function closeDetail() {
  selectedFile.value = null
}

function getFileIcon(type) {
  const icons = {
    'images': '\u{1F5BC}',
    'audio': '\u{1F3B5}',
    'text': '\u{1F4C4}',
    'documents': '\u{1F4C4}',
  }
  return icons[type] || '\u{1F4C1}'
}

function truncate(str, maxLen) {
  if (!str) return ''
  return str.length > maxLen ? str.slice(0, maxLen) + '...' : str
}

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1024 / 1024).toFixed(1) + ' MB'
}

function formatDate(isoString) {
  if (!isoString) return ''
  const date = new Date(isoString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

defineExpose({ fetchFiles })
</script>

<style scoped>
/* ===== 列表区域 ===== */
.file-list-section { margin-top: 20px; }

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.list-header h2 { color: #333; }

.refresh-btn {
  padding: 8px 16px;
  border: 1px solid #667eea;
  background: white;
  color: #667eea;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}
.refresh-btn:hover { background: #667eea; color: white; }
.refresh-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.loading, .empty {
  text-align: center;
  padding: 40px;
  color: #999;
}
.empty-hint { font-size: 13px; margin-top: 8px; color: #bbb; }

/* ===== 文件卡片网格 ===== */
.file-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.file-card {
  border: 1px solid #eee;
  border-radius: 12px;
  overflow: hidden;
  transition: box-shadow 0.3s, transform 0.2s;
  background: white;
  cursor: pointer;
}
.file-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.file-preview {
  height: 150px;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.file-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.file-icon { font-size: 48px; }

.file-info { padding: 12px; }
.file-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.file-meta { font-size: 12px; color: #999; }

/* AI标签 */
.ai-tag {
  margin-top: 6px;
  font-size: 12px;
  color: #667eea;
  background: #f0f4ff;
  padding: 4px 8px;
  border-radius: 12px;
  display: inline-block;
}

/* ===== 操作按钮 ===== */
.file-actions {
  display: flex;
  padding: 0 12px 12px;
  gap: 8px;
}
.action-btn {
  flex: 1;
  padding: 6px 0;
  text-align: center;
  border-radius: 6px;
  font-size: 12px;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}
.action-btn.view { background: #667eea; color: white; }
.action-btn.view:hover { background: #5568d3; }
.action-btn.delete { background: #fee; color: #c33; }
.action-btn.delete:hover { background: #fcc; }

/* ===== 弹窗样式 ===== */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 30px;
  max-width: 400px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from { transform: translateY(30px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.modal-content h3 {
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

/* AI结果展示 */
.ai-tag-large {
  font-size: 18px;
  color: #667eea;
  font-weight: bold;
  margin-bottom: 24px;
  text-align: center;
}

.color-section { margin-bottom: 20px; }
.color-section > p { font-size: 14px; color: #666; margin-bottom: 10px; }

.color-palette {
  display: flex;
  gap: 12px;
}
.color-block {
  width: 56px;
  height: 56px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  transition: transform 0.2s;
}
.color-block:hover { transform: scale(1.1); }

.brightness-bar { margin-bottom: 20px; }
.brightness-bar > p:first-child { font-size: 14px; color: #666; margin-bottom: 8px; }

.bar-track {
  height: 10px;
  background: #eee;
  border-radius: 5px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #333 0%, #ddd 50%, #fff 100%);
  border-radius: 5px;
  transition: width 0.8s ease;
}
.brightness-level {
  font-size: 13px;
  color: #999;
  margin-top: 6px;
}

.dimension {
  color: #666;
  font-size: 14px;
  text-align: center;
  margin-top: 10px;
}

/* 无AI数据 */
.no-ai-data { text-align: center; padding: 20px 0; }
.no-ai-data > p:first-child { color: #999; font-size: 16px; }
.no-ai-hint { font-size: 12px; color: #bbb; margin-top: 6px; }

/* 关闭按钮 */
.close-btn {
  width: 100%;
  padding: 12px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 15px;
  margin-top: 20px;
  transition: background 0.2s;
}
.close-btn:hover { background: #5568d3; }
</style>