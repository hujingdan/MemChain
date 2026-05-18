<template>
  <div class="app-container">
    <header class="app-header">
      <h1>MemChain 时光容器</h1>
      <p class="subtitle">珍藏每一段不可复制的人生故事</p>
    </header>
    <main class="app-main">
      <!-- 上传成功后通知FileList刷新 -->
      <UploadSection @upload-success="onUploadSuccess" />
      <!-- 绑定ref，用于调用子组件方法 -->
      <FileList ref="fileListRef" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import UploadSection from './components/UploadSection.vue'
import FileList from './components/FileList.vue'

const fileListRef = ref(null)

function onUploadSuccess() {
  // 上传成功后刷新文件列表
  fileListRef.value.fetchFiles()
}
</script>

<style>
.app-container { max-width: 1200px; margin: 0 auto; padding: 20px; }
.app-header { text-align: center; color: white; padding: 40px 0; }
.app-header h1 { font-size: 2.5rem; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
.subtitle { font-size: 1.1rem; opacity: 0.9; }
.app-main { background: white; border-radius: 16px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
</style>