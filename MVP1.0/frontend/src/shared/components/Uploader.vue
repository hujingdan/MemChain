/**
 * 核心职责：提供素材上传功能，支持多种类型（图片、音频、文本等），并显示上传进度。
 * 该组件作为通用的上传解决方案，确保文件上传的可靠性、进度反馈和用户体验。
 */

 <template>
  <div class="uploader-container">
    <div class="drop-zone" 
         @dragover.prevent="dragOver = true"
         @dragleave="dragOver = false"
         @drop="onDrop"
         :class="{ 'drag-active': dragOver }"
         @click="triggerFileInput">
      <cloud-upload-icon size="48" />
      <p>{{ dropZoneText }}</p>
      <input type="file" ref="fileInput" 
             multiple :accept="acceptedTypes"
             @change="onFilesSelected" hidden>
    </div>
    
    <div v-if="uploads.length" class="upload-list">
      <div v-for="(upload, index) in uploads" :key="upload.id" class="upload-item">
        <div class="file-info">
          <file-icon :type="upload.type" />
          <span class="filename">{{ upload.name }}</span>
          <span class="size">{{ formatFileSize(upload.size) }}</span>
        </div>
        <div class="status-area">
          <div v-if="upload.error" class="error-badge">
            <alert-circle-icon /> {{ upload.error }}
          </div>
          <progress-bar v-else :value="upload.progress" :max="100" />
          <button v-if="upload.status === 'completed'" class="icon-button" @click="removeUpload(index)">
            <x-icon />
          </button>
        </div>
      </div>
    </div>
    
    <transition name="fade">
      <div v-if="batchStatus" class="batch-status">
        <div class="batch-progress">
          <progress-bar :value="batchProgress" />
          <span>{{ completedCount }}/{{ totalCount }} processed</span>
        </div>
        <div v-if="batchError" class="batch-error">{{ batchError }}</div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios';
import { generateUniqueId } from '@/core/utils/identifier';
import { cloudUpload, file, alertCircle, x } from 'vue-icons';
import ProgressBar from '@/shared/components/ProgressBar.vue';
import FileIcon from '@/shared/components/FileIcon.vue';

export default {
  components: {
    CloudUploadIcon: cloudUpload,
    FileIcon,
    AlertCircleIcon: alertCircle,
    XIcon: x,
    ProgressBar
  },
  props: {
    acceptedTypes: {
      type: Array,
      default: () => ['image/*', 'audio/*', 'text/*']
    },
    chunkSize: {
      type: Number,
      default: 5 * 1024 * 1024 // 5MB chunks
    },
    maxConcurrent: {
      type: Number,
      default: 3
    }
  },
  data() {
    return {
      // 初始化为默认值，将在mounted中更新
      acceptedTypes: ['image/*', 'audio/*', 'text/*'],
      dragOver: false,
      uploads: [],
      batchStatus: null,
      batchProgress: 0,
      batchError: null,
      abortControllers: new Map(),
      uploadQueue: []
    };
  },
  async mounted() {
    // 动态获取后端支持的格式类型
    try {
      const response = await this.$api.get('/upload/supported-types');
      this.acceptedTypes = response.data;
      this.$emit('accepted-types-updated', this.acceptedTypes);
    } catch (error) {
      console.error('Failed to fetch accepted types:', error);
      // 使用默认值但显示警告
      this.$emit('warning', {
        message: 'Using default file types',
        error
      });
    }
  },
  // ...

  computed: {
    dropZoneText() {
      return this.dragOver 
        ? 'Drop files to upload' 
        : 'Click or drag files to upload';
    },
    totalCount() {
      return this.uploads.length;
    },
    completedCount() {
      return this.uploads.filter(u => u.status === 'completed').length;
    },
    activeUploads() {
      return this.uploads.filter(u => 
        u.status === 'uploading' || u.status === 'pending');
    }
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    
    onFilesSelected(event) {
      const files = Array.from(event.target.files);
      this.processFiles(files);
      event.target.value = '';
    },
    
    onDrop(event) {
      this.dragOver = false;
      const files = Array.from(event.dataTransfer.files);
      this.processFiles(files);
      event.preventDefault();
    },
    
    processFiles(files) {
      const validFiles = files.filter(file => 
        this.acceptedTypes.some(type => this.validateFileType(file, type))
      );
      
      if (validFiles.length === 0) {
        this.$emit('error', { type: 'invalid-type', files });
        return;
      }
      
      validFiles.forEach(file => {
        const id = generateUniqueId();
        this.uploads.push({
          id,
          file,
          name: file.name,
          type: file.type || 'application/octet-stream',
          size: file.size,
          progress: 0,
          status: 'pending',
          chunks: Math.ceil(file.size / this.chunkSize),
          completedChunks: 0
        });
      });
      
      this.$emit('files-added', validFiles);
      this.processUploadQueue();
    },
    
    validateFileType(file, pattern) {
      if (pattern === '*/*') return true;
      if (pattern.endsWith('/*')) {
        const category = pattern.split('/')[0];
        return file.type.split('/')[0] === category;
      }
      return file.type === pattern;
    },
    
    async processUploadQueue() {
      while (this.uploadQueue.length > 0 && 
             this.activeUploads.length < this.maxConcurrent) {
        const uploadId = this.uploadQueue.shift();
        await this.uploadFile(uploadId);
      }
    },
    
    async uploadFile(uploadId) {
      const uploadIndex = this.uploads.findIndex(u => u.id === uploadId);
      if (uploadIndex === -1) return;
      
      const upload = this.uploads[uploadIndex];
      upload.status = 'uploading';
      
      const controller = new AbortController();
      this.abortControllers.set(uploadId, controller);
      
      try {
        // 创建上传会话
        const sessionResponse = await this.$api.post('/upload/session', {
          filename: upload.name,
          filetype: upload.type,
          filesize: upload.size
        });
        
        const sessionId = sessionResponse.data.session_id;
        
        // 分片上传
        const chunkCount = Math.ceil(upload.file.size / this.chunkSize);
        for (let chunkIndex = 0; chunkIndex < chunkCount; chunkIndex++) {
          const start = chunkIndex * this.chunkSize;
          const end = Math.min(upload.file.size, start + this.chunkSize);
          const chunk = upload.file.slice(start, end);
          
          const formData = new FormData();
          formData.append('session_id', sessionId);
          formData.append('chunk_index', chunkIndex);
          formData.append('chunk_count', chunkCount);
          formData.append('file', chunk, upload.name);
          
          await axios.put('/upload/chunk', formData, {
            signal: controller.signal,
            onUploadProgress: progressEvent => {
              const chunkProgress = progressEvent.loaded / progressEvent.total;
              const partialProgress = (chunkIndex + chunkProgress) / chunkCount;
              this.updateProgress(uploadId, partialProgress * 100);
            }
          });
          
          this.uploads[uploadIndex].completedChunks++;
        }
        
        // 完成上传
        const completionResponse = await this.$api.post('/upload/complete', {
          session_id: sessionId,
          metadata: this.extractMetadata(upload.file)
        });
        
        this.uploads[uploadIndex].status = 'completed';
        this.uploads[uploadIndex].progress = 100;
        this.uploads[uploadIndex].materialId = completionResponse.data.material_id;
        
        this.$emit('upload-completed', completionResponse.data);
        this.calculateBatchProgress();
      } catch (error) {
        if (axios.isCancel(error)) {
          this.uploads[uploadIndex].status = 'canceled';
        } else {
          this.uploads[uploadIndex].status = 'error';
          this.uploads[uploadIndex].error = this.getErrorMessage(error);
          this.batchError = `Upload failed: ${this.getErrorMessage(error)}`;
          this.$emit('error', { error, upload });
        }
      } finally {
        this.abortControllers.delete(uploadId);
        this.processUploadQueue();
      }
    },
    
    extractMetadata(file) {
      return {
        name: file.name,
      };
    },
    
    getErrorMessage(error) {
      if (error.response) {
        return error.response.data.error || `Server error: ${error.response.status}`;
      }
      return error.message || 'Unknown error';
    },
    
    updateProgress(uploadId, progress) {
      const uploadIndex = this.uploads.findIndex(u => u.id === uploadId);
      if (uploadIndex !== -1) {
        this.uploads[uploadIndex].progress = progress;
        this.calculateBatchProgress();
      }
    },
    
    calculateBatchProgress() {
      if (this.totalCount === 0) return;
      
      const totalProgress = this.uploads.reduce((sum, upload) => 
        sum + (upload.progress / this.totalCount), 0);
      this.batchProgress = Math.round(totalProgress);
      this.batchStatus = this.completedCount === this.totalCount 
        ? 'completed' : 'processing';
    },
    
    removeUpload(index) {
      const upload = this.uploads[index];
      if (this.abortControllers.has(upload.id)) {
        this.abortControllers.get(upload.id).abort();
      }
      this.uploads.splice(index, 1);
      this.calculateBatchProgress();
    },
    
    formatFileSize(bytes) {
      // File size formatting implementation
    }
  },
  watch: {
    uploads: {
      handler() {
        // 为pending文件启动上传
        const pendingUploads = this.uploads
          .filter(u => u.status === 'pending')
          .map(u => u.id);
          
        this.uploadQueue = [...this.uploadQueue, ...pendingUploads];
        this.processUploadQueue();
      },
      deep: true
    }
  }
};
</script>

<style scoped>
/* 专业级上传界面样式 */
.uploader-container {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem;
}

.drop-zone {
  border: 2px dashed var(--border-color);
  border-radius: 8px;
  padding: 3rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.drag-active {
  border-color: var(--primary-color);
  background-color: color-mix(in srgb, var(--primary-color) 10%, transparent);
}

.upload-list {
  margin-top: 1.5rem;
  max-height: 300px;
  overflow-y: auto;
}

.upload-item {
  border-bottom: 1px solid var(--border-color);
  padding: 0.75rem 0;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.filename {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
}

.status-area {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.error-badge {
  color: var(--error-color);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.icon-button {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-secondary);
}

.batch-status {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.batch-progress {
  display: flex;
  align-items: center;
  gap: 1rem;
}
</style>