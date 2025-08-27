import { useState } from 'react';
import { cn } from '@/lib/utils';
import { motion, AnimatePresence } from 'framer-motion';

// 筛选选项数据
const filterOptions = {
  type: [
    { id: 'photo', name: '照片', icon: 'fa-image' },
    { id: 'recording', name: '录音', icon: 'fa-microphone' },
    { id: 'note', name: '笔记', icon: 'fa-file-text' }
  ],
  emotions: [
    { id: 'happy', name: '开心', color: 'text-amber-500', icon: 'fa-face-laugh-beam' },
    { id: 'calm', name: '平静', color: 'text-blue-500', icon: 'fa-face-meh' },
    { id: 'sad', name: '低落', color: 'text-gray-500', icon: 'fa-face-sad-tear' },
    { id: 'excited', name: '激动', color: 'text-red-500', icon: 'fa-face-surprise' },
    { id: 'warm', name: '温暖', color: 'text-orange-500', icon: 'fa-face-smile' }
  ],
  // 在实际应用中，这些数据会从API获取或从用户数据中提取
  people: [
    { id: 'self', name: '自己' },
    { id: 'family', name: '家人' },
    { id: 'friends', name: '朋友' },
    { id: 'colleagues', name: '同事' }
  ],
  location: [
    { id: 'home', name: '家中' },
    { id: 'work', name: '工作场所' },
    { id: 'school', name: '学校' },
    { id: 'park', name: '公园' },
    { id: 'travel', name: '旅行地' }
  ],
  tags: [
    { id: 'family', name: '家庭' },
    { id: 'travel', name: '旅行' },
    { id: 'nature', name: '自然' },
    { id: 'study', name: '学习' },
    { id: 'work', name: '工作' },
    { id: 'memories', name: '回忆' }
  ]
};

// 筛选工具栏组件
interface FilterToolbarProps {
  filters: {
    type: string[];
    people: string[];
    location: string[];
    emotions: string[];
    tags: string[];
  };
  onFilterChange: (filterType: string, values: string[]) => void;
  className?: string;
}

export default function FilterToolbar({ filters, onFilterChange, className = "" }: FilterToolbarProps) {
  const [openFilter, setOpenFilter] = useState<string | null>(null);
  
  // 处理筛选项点击
  const handleFilterItemClick = (filterType: string, itemId: string) => {
    const currentValues = [...filters[filterType as keyof typeof filters]];
    const index = currentValues.indexOf(itemId);
    
    if (index > -1) {
      currentValues.splice(index, 1);
    } else {
      currentValues.push(itemId);
    }
    
    onFilterChange(filterType, currentValues);
  };
  
  // 渲染筛选弹窗内容
  const renderFilterContent = (filterType: string) => {
    const options = filterOptions[filterType as keyof typeof filterOptions];
    const currentValues = filters[filterType as keyof typeof filters];
    
    return (
      <div className="p-4 space-y-3">
        <h3 className="font-medium text-gray-800 dark:text-gray-200 mb-2">
          {filterType === 'type' && '数据类型'}
          {filterType === 'people' && '人物'}
          {filterType === 'location' && '地点'}
          {filterType === 'emotions' && '情绪'}
          {filterType === 'tags' && '标签'}
        </h3>
        <div className={
          filterType === 'emotions' 
            ? "grid grid-cols-2 sm:grid-cols-3 gap-2" 
            : "grid grid-cols-2 sm:grid-cols-3 md:grid-cols-2 gap-2"
        }>
          {options.map((option: any) => (
            <button
              key={option.id}
              onClick={() => handleFilterItemClick(filterType, option.id)}
              className={cn(
                "flex items-center justify-center px-3 py-2 rounded-lg text-sm transition-colors",
                currentValues.includes(option.id)
                  ? "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100"
                  : "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-700"
              )}
            >
              {option.icon && (
                <i className={`fa-solid ${option.icon} ${option.color || ''} mr-2`}></i>
              )}
              {option.name}
            </button>
          ))}
        </div>
        <div className="pt-2 flex justify-end">
          <button
            onClick={() => onFilterChange(filterType, [])}
            className="text-sm text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400"
          >
            清除全部
          </button>
        </div>
      </div>
    );
  };
  
  // 获取活跃筛选器的数量
  const getActiveFilterCount = () => {
    return Object.values(filters).reduce((total, values) => total + values.length, 0);
  };
  
  return (
    <div className={cn("bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-2", className)}>
      <div className="flex flex-wrap items-center gap-2">
        {/* 筛选按钮组 */}
        {Object.keys(filters).map((filterType) => (
          <button
            key={filterType}
            onClick={() => setOpenFilter(openFilter === filterType ? null : filterType)}
            className={cn(
              "flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-colors relative",
              openFilter === filterType
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600"
            )}
          >
            {filterType === 'type' && (
              <>
                <i className="fa-solid fa-cubes mr-2"></i>类型
              </>
            )}
            {filterType === 'people' && (
              <>
                <i className="fa-solid fa-users mr-2"></i>人物
              </>
            )}
            {filterType === 'location' && (
              <>
                <i className="fa-solid fa-map-marker-alt mr-2"></i>地点
              </>
            )}
            {filterType === 'emotions' && (
              <>
                <i className="fa-solid fa-face-smile mr-2"></i>情绪
              </>
            )}
            {filterType === 'tags' && (
              <>
                <i className="fa-solid fa-tags mr-2"></i>标签
              </>
            )}
            
            {/* 选中数量指示 */}
            {filters[filterType as keyof typeof filters].length > 0 && (
              <span className="ml-1 inline-flex items-center justify-center w-4 h-4 rounded-full text-[10px] bg-white text-blue-600 dark:bg-gray-900">
                {filters[filterType as keyof typeof filters].length}
              </span>
            )}
            
            <i className={`fa-solid fa-chevron-down ml-1 text-xs transition-transform ${openFilter === filterType ? 'rotate-180' : ''}`}></i>
            
            {/* 筛选弹窗 */}
            <AnimatePresence>
              {openFilter === filterType && (
                <motion.div
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 5 }}
                  className="absolute top-full left-0 mt-1 w-64 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-10"
                  onClick={(e) => e.stopPropagation()}
                >
                  {renderFilterContent(filterType)}
                </motion.div>
              )}
            </AnimatePresence>
          </button>
        ))}
        
        {/* 已选筛选器显示 */}
        {getActiveFilterCount() > 0 && (
          <div className="ml-auto flex items-center">
            <button
              onClick={() => {
                Object.keys(filters).forEach(filterType => {
                  onFilterChange(filterType, []);
                });
              }}
              className="flex items-center px-3 py-2 text-sm text-gray-600 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400"
            >
              <i className="fa-solid fa-times-circle mr-1"></i>
              清除全部筛选
            </button>
          </div>
        )}
      </div>
    </div>
  );
}