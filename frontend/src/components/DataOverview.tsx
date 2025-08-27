import { motion } from 'framer-motion';

// 数据概览组件
interface DataOverviewProps {
  data: {
    photos: number;
    recordings: number;
    notes: number;
  };
}

export default function DataOverview({ data }: DataOverviewProps) {
  const stats = [
    { label: "照片", value: data.photos, icon: "fa-image", color: "text-blue-500" },
    { label: "录音", value: data.recordings, icon: "fa-microphone", color: "text-purple-500" },
    { label: "笔记", value: data.notes, icon: "fa-file-text", color: "text-amber-500" },
    { label: "总记忆", value: data.photos + data.recordings + data.notes, icon: "fa-database", color: "text-emerald-500" },
  ];
  
  return (
    <section className="mb-16 bg-white dark:bg-gray-800 rounded-2xl shadow-md p-6 md:p-8 border border-gray-100 dark:border-gray-700">
      <h2 className="text-2xl font-bold text-center mb-8 text-gray-800 dark:text-gray-200">
        您的记忆收藏
      </h2>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <motion.div 
            key={index}
            className="text-center p-4 rounded-xl bg-gray-50 dark:bg-gray-700/50"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <div className={`text-3xl ${stat.color} mb-2`}>
              <i className={`fa-solid ${stat.icon}`}></i>
            </div>
            <p className="text-3xl font-bold text-gray-800 dark:text-white">{stat.value}</p>
            <p className="text-gray-600 dark:text-gray-400">{stat.label}</p>
          </motion.div>
        ))}
      </div>
      
      <div className="mt-8 text-center">
        <button className="inline-flex items-center px-5 py-2.5 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-full font-medium hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors">
          <i className="fa-solid fa-plus mr-2"></i>导入更多记忆
        </button>
      </div>
    </section>
  );
}