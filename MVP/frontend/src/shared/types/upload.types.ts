/**
 * 上传相关的类型定义
 */

// 文件上传状态枚举
export enum UploadStatus {
  PENDING = 'pending',
  UPLOADING = 'uploading',
  SUCCESS = 'success',
  ERROR = 'error'
}

// 上传文件的元数据
export interface FileMetadata {
  id: string
  name: string
  size: number
  type: string
  lastModified: number
  status: UploadStatus
  progress: number
  url?: string
  error?: string
}

// 上传配置选项
export interface UploadOptions {
  // 允许的文件类型
  accept?: string[]
  // 最大文件大小（字节）
  maxSize?: number
  // 是否允许多文件上传
  multiple?: boolean
  // 是否自动开始上传
  autoUpload?: boolean
  // 是否显示预览
  showPreview?: boolean
}

// 上传响应类型
export interface UploadResponse {
  id: string
  url: string
  metadata: Record<string, any>
}
