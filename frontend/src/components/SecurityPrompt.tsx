import { motion } from 'framer-motion';

// 安全提示组件
export default function SecurityPrompt() {
  return (
    <motion.section 
      className="mb-16 rounded-2xl overflow-hidden bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 p-8 border border-gray-200 dark:border-gray-700"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex flex-col md:flex-row items-center">
        <div className="md:w-1/3 mb-6 md:mb-0 md:pr-8">
          <div className="w-16 h-16 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mx-auto md:mx-0">
            <i className="fa-solid fa-shield text-2xl text-blue-600 dark:text-blue-400"></i>
          </div>
        </div>
        
        <div className="md:w-2/3 text-center md:text-left">
          <h2 className="text-2xl font-bold mb-3 text-gray-800 dark:text-gray-200">您的数据安全由您掌控</h2>
          <p className="text-gray-600 dark:text-gray-300 max-w-2xl">
            本地数据仅本地处理，云端数据加密存储。您可以随时切换存储模式，完全掌控自己的人生记忆数据。
          </p>
          <div className="mt-4 flex justify-center md:justify-start space-x-4">
            <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-full text-sm font-medium transition-colors">
              <i className="fa-solid fa-lock mr-1"></i> 安全设置
            </button>
            <button className="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-full text-sm font-medium transition-colors">
              了解更多
            </button>
          </div>
        </div>
      </div>
    </motion.section>
  );
}