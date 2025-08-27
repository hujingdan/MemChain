import { useState } from 'react';
import { motion } from 'framer-motion';
import FilterToolbar from '@/components/FilterToolbar';
import Timeline from '@/components/Timeline';
import MemoryCard from '@/components/MemoryCard';
import { cn } from '@/lib/utils';
import Navbar from '@/components/Navbar';

// 模拟记忆数据
const mockMemories = [
  {
    id: 1,
    type: 'photo',
    title: '大学毕业典礼',
    date: '2023-06-20',
    location: '学校礼堂',
    people: ['自己', '同学', '导师'],
    emotions: ['开心', '激动'],
    tags: ['毕业', '大学', '重要时刻'],
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_16_9&prompt=university%20graduation%20ceremony%20photo&sign=7178df85e698705997b72ddbf89dd823',
    description: '四年大学生活的终点，也是人生新阶段的起点。'
  },
  {
    id: 2,
    type: 'note',
    title: '第一次独自旅行',
    date: '2023-07-15',
    location: '云南大理',
    people: ['自己'],
    emotions: ['平静', '自由'],
    tags: ['旅行', '独自', '成长'],
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_16_9&prompt=travel%20journal%20with%20mountains%20and%20lakes&sign=a0764345a9a11df2282b12f293fda83b',
    description: '第一次完全独自的旅行，学会了与自己相处，看到了不一样的风景。'
  },
  {
    id: 3,
    type: 'recording',
    title: '奶奶的故事',
    date: '2023-09-03',
    location: '老家',
    people: ['自己', '奶奶'],
    emotions: ['温暖', '怀念'],
    tags: ['家庭', '故事', '亲情'], 
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_16_9&prompt=old%20woman%20telling%20stories%20with%20warm%20lighting&sign=bce30bffd21ae2d38e0d4abd2550206f',
    description: '记录了奶奶讲述她年轻时的经历，珍贵的声音记忆。'
  },
  {
    id: 4,
    type: 'photo',
    title: '初雪',
    date: '2023-12-10',
    location: '城市公园',
    people: ['自己'],
    emotions: ['平静', '喜悦'],
    tags: ['自然', '季节', '美景'],
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_16_9&prompt=first%20snow%20in%20winter%20park&sign=3646ee1033271b921a5881af81337e49',
    description: '今年的第一场雪，整个城市都安静下来了。'
  },
  {
    id: 5,
    type: 'note',
    title: '新年计划',
    date: '2024-01-01',
    location: '家中',
    people: ['自己'],
    emotions: ['期待', '决心'],
    tags: ['计划', '新年', '目标'],
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_16_9&prompt=new%20year%20resolutions%20written%20in%20notebook&sign=9cfffb8f86e6ee76cc86a52893f2350f',
    description: '新的一年，希望自己能够更加勇敢，尝试更多新事物。'
  }
];

// 模拟时间轴数据
const timelineData = [
  { year: 2023, months: [6, 7, 9, 12] },
  { year: 2024, months: [1] }
];

// 时光流页面组件
export default function TimeStream() {
  // 状态管理
  const [activeView, setActiveView] = useState<'year' | 'month' | 'day'>('month');
  const [selectedDate, setSelectedDate] = useState<string>('2023-06');
  const [filters, setFilters] = useState({
    type: [],
    people: [],
    location: [],
    emotions: [],
    tags: []
  });
  const [memories, setMemories] = useState(mockMemories);
  
  // 处理时间轴节点选择
  const handleDateSelect = (date: string) => {
    setSelectedDate(date);
    // 在实际应用中，这里会根据选择的日期筛选记忆数据
  };
  
  // 处理筛选条件变更
  const handleFilterChange = (filterType: string, values: string[]) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: values
    }));
    // 在实际应用中，这里会根据筛选条件过滤记忆数据
  };
  
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 text-gray-900 dark:text-gray-100">
      {/* 导航栏 */} 
      <Navbar />
      
      {/* 页面标题区域 */}
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-700 dark:from-blue-400 dark:to-indigo-500 mb-2">
            时光流
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            沿着时间的轨迹，重温您的珍贵记忆
          </p>
        </div>
        
        {/* 筛选工具栏 */}
        <FilterToolbar 
          filters={filters} 
          onFilterChange={handleFilterChange}
          className="mb-8"
        />
        
        {/* 时间轴控制与显示 */}
        <div className="mb-10">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-200">
              {selectedDate} 的记忆
            </h2>
            <div className="flex space-x-2">
              <button 
                onClick={() => setActiveView('year')}
                className={cn(
                  'px-4 py-2 rounded-full text-sm font-medium transition-colors',
                  activeView === 'year' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600'
                )}
              >
                年视图
              </button>
              <button 
                onClick={() => setActiveView('month')}
                className={cn(
                  'px-4 py-2 rounded-full text-sm font-medium transition-colors',
                  activeView === 'month' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600'
                )}
              >
                月视图
              </button>
              <button 
                onClick={() => setActiveView('day')}
                className={cn(
                  'px-4 py-2 rounded-full text-sm font-medium transition-colors',
                  activeView === 'day' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600'
                )}
              >
                日视图
              </button>
            </div>
          </div>
          
          {/* 时间轴组件 */}
          <Timeline 
            data={timelineData} 
            activeView={activeView}
            selectedDate={selectedDate}
            onDateSelect={handleDateSelect}
          />
        </div>
        
        {/* 记忆卡片预览区 */}
        <div>
          <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-6">
            记忆收藏 ({memories.length})
          </h2>
          
          {memories.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {memories.map(memory => (
                <MemoryCard key={memory.id} memory={memory} />
              ))}
            </div>
          ) : (
            <div className="text-center py-16 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
              <i className="fa-solid fa-clock-rotate-left text-4xl text-gray-400 mb-4"></i>
              <h3 className="text-xl font-medium text-gray-700 dark:text-gray-300 mb-2">暂无记忆数据</h3>
              <p className="text-gray-500 dark:text-gray-400 mb-6">该时间段内没有找到匹配的记忆</p>
              <button className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-full font-medium transition-colors">
                <i className="fa-solid fa-plus mr-2"></i>添加新记忆
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}