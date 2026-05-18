<template>
  <div class="upload-section">
    <h2>上传记忆素材</h2>
    
    <!-- 拖拽上传区域 -->
    <div
      class="upload-zone"
      :class="{ 'drag-over': isDragOver }"
      @click="triggerFileInput"
      @dragover.prevent="isDragOver = true"
      @dragleave="isDragOver = false"
      @drop.prevent="handleDrop"
    >
      <input
        ref="fileInput"
        type="file"
        hidden
        @change="handleFileSelect"
      />
      <div class="upload-icon">+</div>
      <p class="upload-text">
        {{ isUploading ? '上传中...' : '点击或拖拽文件到此处上传' }}
      </p>
      <p class="upload-hint">支持图片、音频、文本、PDF，最大10MB</p>
    </div>

    <!-- 上传状态提示 -->
    <div v-if="message" class="message" :class="messageType">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// ===== 响应式状态 =====
const fileInput = ref(null)       // 引用隐藏的input元素
const isDragOver = ref(false)     // 是否正在拖拽悬停
const isUploading = ref(false)    // 是否正在上传
const message = ref('')           // 提示信息
const messageType = ref('')       // 提示类型：success / error

// 定义触发事件（供父组件监听）
const emit = defineEmits(['upload-success'])

// ===== API配置 =====
const API_BASE = 'http://localhost:8000'

// ===== 方法 =====

// 点击上传区域时触发隐藏的input
function triggerFileInput() {
  fileInput.value.click()
}

// 处理input选择的文件
function handleFileSelect(event) {
  const file = event.target.files[0]
  if (file) uploadFile(file)
}

// 处理拖拽 dropped 的文件
function handleDrop(event) {
  isDragOver.value = false
  const file = event.dataTransfer.files[0]
  if (file) uploadFile(file)
}

// 执行上传
async function uploadFile(file) {
  // 文件大小检查（10MB）
  if (file.size > 10 * 1024 * 1024) {
    showMessage('文件过大，最大支持10MB', 'error')
    return
  }

  isUploading.value = true
  message.value = ''

  // 构造表单数据
  const formData = new FormData()
  formData.append('file', file)  // 'file' 必须与后端UploadFile参数名一致

  try {
    const response = await fetch(`${API_BASE}/upload/`, {
      method: 'POST',
      body: formData
      // 注意：Content-Type不要手动设置，浏览器会自动设置并带上boundary
    })

    const result = await response.json()

    if (response.ok && result.success) {
      showMessage(`上传成功！文件ID: ${result.data.id.slice(0, 8)}...`, 'success')
      emit('upload-success')  // 通知父组件刷新列表
    } else {
      showMessage(result.detail || result.error || '上传失败', 'error')
    }
  } catch (err) {
    showMessage('网络错误，请确保后端服务已启动', 'error')
  } finally {
    isUploading.value = false
    // 清空input，允许重复上传同一文件
    fileInput.value.value = ''
  }
}

// 显示提示信息
function showMessage(text, type) {
  message.value = text
  messageType.value = type
  // 3秒后自动清除
  setTimeout(() => { message.value = '' }, 3000)
}
</script>

<style scoped>
.upload-section {
  margin-bottom: 30px;
}

.upload-section h2 {
  margin-bottom: 15px;
  color: #333;
}

.upload-zone {
  border: 2px dashed #ccc;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #fafafa;
}

.upload-zone:hover {
  border-color: #667eea;
  background: #f0f4ff;
}

.upload-zone.drag-over {
  border-color: #667eea;
  background: #e8eeff;
  transform: scale(1.02);
}

.upload-icon {
  font-size: 48px;
  color: #667eea;
  margin-bottom: 10px;
}

.upload-text {
  font-size: 16px;
  color: #555;
  margin-bottom: 8px;
}

.upload-hint {
  font-size: 12px;
  color: #999;
}

.message {
  margin-top: 15px;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
}

.message.success {
  background: #d4edda;
  color: #155724;
}

.message.error {
  background: #f8d7da;
  color: #721c24;
}
</style>