import { motion } from 'framer-motion';

// 功能卡片组件
import { useNavigate } from 'react-router-dom';

interface FeatureCardProps {
  title: string;
  description: string;
  icon: string;
  color: string;
  imageUrl: string;
  path?: string;
}

export default function FeatureCard({ title, description, icon, color, imageUrl, path }: FeatureCardProps) {
  const navigate = useNavigate();
  return (
    <motion.div 
      className="group rounded-xl overflow-hidden bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 dark:border-gray-700"
      whileHover={{ y: -5 }}
    >
      {/* 卡片图片区域 */}
      <div className="relative h-48 overflow-hidden">
        <img 
          src={imageUrl} 
          alt={title} 
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-70"></div>
        <div className="absolute bottom-4 left-4 text-white">
          <div className={`w-12 h-12 rounded-full bg-gradient-to-r ${color} flex items-center justify-center mb-2`}>
            <i className={`fa-solid ${icon} text-xl`}></i>
          </div>
          <h3 className="text-xl font-bold">{title}</h3>
        </div>
      </div>
      
      {/* 卡片内容区域 */}
      <div className="p-6">
        <p className="text-gray-600 dark:text-gray-300 mb-4">{description}</p>
        <button 
          className="inline-flex items-center text-blue-600 dark:text-blue-400 font-medium hover:underline"
          onClick={() => path && navigate(path)}
        >
          探索功能
          <i className="fa-solid fa-arrow-right ml-2 text-sm transition-transform group-hover:translate-x-1"></i>
        </button>
      </div>
    </motion.div>
  );
}