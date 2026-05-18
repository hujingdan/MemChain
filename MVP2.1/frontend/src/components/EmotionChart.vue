<template>
  <div class="emotion-chart-wrapper">
    <div class="chart-header">
      <h3 class="chart-title">情绪时间轴</h3>
      <div class="chart-period">
        <button
          v-for="p in periods"
          :key="p.days"
          class="period-btn"
          :class="{ active: selectedPeriod === p.days }"
          @click="changePeriod(p.days)"
        >
          {{ p.label }}
        </button>
      </div>
    </div>
    <v-chart
      class="emotion-chart"
      :option="chartOption"
      autoresize
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent, DataZoomComponent } from 'echarts/components'
import VChart from 'vue-echarts'
import { EMOTION_MAP } from '../shared/constants.js'
import { API_BASE } from '../shared/constants.js'

// 注册ECharts组件
use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent, DataZoomComponent])

const periods = [
  { days: 7, label: '7天' },
  { days: 30, label: '30天' },
  { days: 90, label: '90天' },
]

const selectedPeriod = ref(30)
const emotionData = ref({ dates: [], scores: [], emotions: [] })
const loading = ref(false)

// 获取情绪数据
async function fetchEmotions(days) {
  loading.value = true
  try {
    const response = await fetch(`${API_BASE}/timeline/emotions?days=${days}`)
    const result = await response.json()
    if (result.success) {
      emotionData.value = result.data
    }
  } catch (err) {
    console.error('获取情绪数据失败:', err)
  } finally {
    loading.value = false
  }
}

function changePeriod(days) {
  selectedPeriod.value = days
  fetchEmotions(days)
}

// ECharts配置
const chartOption = computed(() => {
  const { dates, scores, emotions } = emotionData.value
  
  return {
    grid: {
      left: 50, right: 30, top: 30, bottom: 40
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#F0D5D0',
      borderWidth: 1,
      textStyle: { color: '#3D3D3D' },
      formatter: (params) => {
        const idx = params[0].dataIndex
        const em = emotions[idx]
        return `
          <div style="padding:4px;">
            <div style="font-weight:600;margin-bottom:4px;">${dates[idx]}</div>
            <div style="display:flex;align-items:center;gap:6px;">
              <span style="font-size:16px;">${em?.icon || ''}</span>
              <span style="color:${em?.color || '#999'}">${em?.label || '未知'}</span>
              <span style="font-weight:600;">(${scores[idx]})</span>
            </div>
          </div>
        `
      }
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: '#F0D5D0' } },
      axisLabel: { color: '#888', fontSize: 11 },
      axisTick: { show: false },
    },
    yAxis: {
      type: 'value',
      min: -100,
      max: 100,
      interval: 50,
      axisLine: { show: false },
      splitLine: { lineStyle: { color: '#F5E5E0', type: 'dashed' } },
      axisLabel: { color: '#888', fontSize: 11 },
    },
    series: [{
      type: 'line',
      data: scores,
      smooth: true,  // 平滑曲线
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: {
        color: '#E88B7C',
        width: 3,
      },
      itemStyle: {
        color: '#E88B7C',
        borderColor: '#fff',
        borderWidth: 2,
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(232,139,124,0.25)' },
            { offset: 1, color: 'rgba(232,139,124,0.02)' },
          ],
        },
      },
      emphasis: {
        itemStyle: {
          color: '#D47366',
          borderColor: '#fff',
          borderWidth: 3,
          shadowBlur: 10,
          shadowColor: 'rgba(232,139,124,0.4)',
        },
      },
    }],
    animationDuration: 800,
    animationEasing: 'cubicOut',
  }
})

onMounted(() => {
  fetchEmotions(30)
})

watch(selectedPeriod, (newVal) => {
  fetchEmotions(newVal)
})
</script>

<style scoped>
.emotion-chart-wrapper {
  background: var(--bg-card);
  border-radius: var(--card-radius);
  padding: 20px 24px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-sm);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.chart-period {
  display: flex;
  gap: 4px;
  background: var(--bg-hover);
  padding: 4px;
  border-radius: 8px;
}

.period-btn {
  padding: 6px 14px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  color: var(--text-secondary);
  background: transparent;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.period-btn:hover {
  color: var(--primary);
}

.period-btn.active {
  background: var(--bg-card);
  color: var(--primary);
  font-weight: 500;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.emotion-chart {
  height: 280px;
  width: 100%;
}
</style>