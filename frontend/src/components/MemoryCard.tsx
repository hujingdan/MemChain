import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

// 记忆卡片属性
interface MemoryProps {
  id: number;
  type: 'photo' | 'recording' | 'note';
  title: string;
  date: string;
  location: string;
  people: string[];
  emotions: string[];
  tags: string[];
  thumbnail: string;
  description: string;
}

// 记忆卡片组件
interface MemoryCardProps {
  memory: MemoryProps;
}

// 获取记忆类型图标
const getMemoryTypeIcon = (type: string) => {
  switch (type) {
    case 'photo':
      return <i className="fa-solid fa-image text-blue-500"></i>;
    case 'recording':
      return <i className="fa-solid fa-microphone text-purple-500"></i>;
    case 'note':
      return <i className="fa-solid fa-file-text text-amber-500"></i>;
    default:
      return <i className="fa-solid fa-circle-question text-gray-400"></i>;
  }
};

// 获取情绪标签样式
const getEmotionColor = (emotion: string) => {
  switch (emotion) {
    case '开心':
      return 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400';
    case '平静':
      return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400';
    case '低落':
      return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300';
    case '激动':
      return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400';
    case '温暖':
      return 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400';
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300';
  }
  
};

export default function MemoryCard({ memory }: MemoryCardProps) {
  // 格式化日期显示
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };
  
  return (
    <motion.div 
      className="group bg-white dark:bg-gray-800 rounded-xl overflow-hidden shadow-md hover:shadow-xl transition-all duration-300 border border-gray-200 dark:border-gray-700"
      whileHover={{ y: -5 }}
    >
      {/* 记忆缩略图区域 */}
      <div className="relative h-48 overflow-hidden">
        <img 
          src={memory.thumbnail} 
          alt={memory.title} 
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
        />
        <div className="absolute top-3 left-3">
          <div className="w-10 h-10 rounded-full bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm flex items-center justify-center shadow-md">
            {getMemoryTypeIcon(memory.type)}
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent p-4">
          <div className="flex justify-between items-end">
            <h3 className="text-xl font-bold text-white">{memory.title}</h3>
            <span className="text-sm text-gray-200">{formatDate(memory.date)}</span>
          </div>
        </div>
      </div>
      
      {/* 记忆信息区域 */}
      <div className="p-4">
        {/* 情绪标签 */}
        <div className="flex flex-wrap gap-2 mb-3">
          {memory.emotions.map(emotion => (
            <span key={emotion} className={`text-xs px-2.5 py-1 rounded-full ${getEmotionColor(emotion)}`}>
              {emotion}
            </span>
          ))}
        </div>
        
        {/* 描述文字 */}
        <p className="text-gray-600 dark:text-gray-300 text-sm line-clamp-2 mb-4">
          {memory.description}
        </p>
        
        {/* 位置和人物信息 */}
        <div className="flex items-center text-xs text-gray-500 dark:text-gray-400 mb-4">
          {memory.location && (
            <div className="flex items-center mr-4">
              <i className="fa-solid fa-map-marker-alt mr-1"></i>
              {memory.location}
            </div>
          )}
          {memory.people.length > 0 && (
            <div className="flex items-center">
              <i className="fa-solid fa-user mr-1"></i>
              {memory.people.join(', ')}
            </div>
          )}
        </div>
        
        {/* 标签和操作区 */}
        <div className="flex justify-between items-center pt-3 border-t border-gray-100 dark:border-gray-700">
          <div className="flex flex-wrap gap-1">
            {memory.tags.slice(0, 2).map(tag => (
              <span key={tag} className="text-xs px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full">
                #{tag}
              </span>
            ))}
            {memory.tags.length > 2 && (
              <span className="text-xs px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full">
                +{memory.tags.length - 2}
              </span>
            )}
          </div>
          
          <div className="flex space-x-2">
            <button className="p-2 text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              <i className="fa-solid fa-eye"></i>
            </button>
            <button className="p-2 text-gray-500 hover:text-amber-500 dark:text-gray-400 dark:hover:text-amber-400 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              <i className="fa-solid fa-heart"></i>
            </button>
            <button className="p-2 text-gray-500 hover:text-green-600 dark:text-gray-400 dark:hover:text-green-400 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              <i className="fa-solid fa-ellipsis-vertical"></i>
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
}