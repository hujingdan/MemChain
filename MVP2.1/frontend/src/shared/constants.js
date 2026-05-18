/**
 * constants.js - 前端全局常量
 * 必须与后端 core/global_constants.py 保持完全一致！
 * 修改时需同步更新后端。
 */

// ========== 情绪标签体系 ==========
export const EMOTION_MAP = {
  ecstasy:      { score: 100, label: '狂喜', color: '#FF6B6B', icon: '\u{1F929}' },
  joy:          { score: 75,  label: '开心', color: '#FFD93D', icon: '\u{1F600}' },
  content:      { score: 40,  label: '平静', color: '#6BCB77', icon: '\u{1F60C}' },
  neutral:      { score: 0,   label: '平淡', color: '#B8B8B8', icon: '\u{1F610}' },
  disappointed: { score: -40, label: '失落', color: '#9FB4CC', icon: '\u{1F614}' },
  sad:          { score: -65, label: '难过', color: '#5B8DB8', icon: '\u{1F622}' },
  angry:        { score: -85, label: '愤怒', color: '#E84545', icon: '\u{1F620}' },
  despair:      { score: -100,label: '绝望', color: '#4A0E0E', icon: '\u{1F62D}' },
}

/** 根据分值获取最近的情绪 */
export function getEmotionByScore(score) {
  let closest = null
  let minDiff = Infinity
  for (const [key, val] of Object.entries(EMOTION_MAP)) {
    const diff = Math.abs(val.score - score)
    if (diff < minDiff) {
      minDiff = diff
      closest = { key, ...val }
    }
  }
  return closest
}

/** 获取所有情绪列表（按分值从高到低） */
export function getAllEmotions() {
  return Object.entries(EMOTION_MAP)
    .map(([key, val]) => ({ key, ...val }))
    .sort((a, b) => b.score - a.score)
}

// ========== 天气类型 ==========
export const WEATHER_TYPES = [
  { key: 'sunny',   label: '晴朗', icon: '\u2600' },
  { key: 'cloudy',  label: '多云', icon: '\u2601' },
  { key: 'rainy',   label: '下雨', icon: '\u{1F327}' },
  { key: 'snowy',   label: '下雪', icon: '\u2744' },
  { key: 'windy',   label: '大风', icon: '\u{1F32C}' },
  { key: 'foggy',   label: '雾霾', icon: '\u{1F32B}' },
  { key: 'thunder', label: '雷雨', icon: '\u26C8' },
]

// ========== 系统预设标签 ==========
export const SYSTEM_TAGS = [
  { name: '家庭', color: '#E88B7C' },
  { name: '工作', color: '#5B8DB8' },
  { name: '旅行', color: '#6BCB77' },
  { name: '健康', color: '#FFD93D' },
  { name: '回忆', color: '#C9B1FF' },
  { name: '学习', color: '#FF9F45' },
  { name: '美食', color: '#FF6B6B' },
  { name: '友情', color: '#95D1CC' },
]

// ========== API配置 ==========
export const API_BASE = 'http://localhost:8000'

// ========== 分页默认值 ==========
export const DEFAULT_PAGE_SIZE = 20
export const MAX_PAGE_SIZE = 100

// ========== 存储限额 ==========
export const DEFAULT_STORAGE_LIMIT = 1024 * 1024 * 1024 // 1GB