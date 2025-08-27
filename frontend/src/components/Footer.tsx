// 页脚组件
export default function Footer() {
  return (
    <footer className="bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 py-8">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-6 md:mb-0">
            <div className="flex items-center justify-center md:justify-start">
              <i className="fa-solid fa-link text-xl text-blue-600 dark:text-blue-400 mr-2"></i>
              <span className="text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-700 dark:from-blue-400 dark:to-indigo-500">MemChain</span>
            </div>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-2 text-center md:text-left">
              人生博物馆 © {new Date().getFullYear()}
            </p>
          </div>
          
          <div className="flex space-x-6">
            <a href="#" className="text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 transition-colors">
              <i className="fa-solid fa-question-circle mr-1"></i>帮助中心
            </a>
            <a href="#" className="text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 transition-colors">
              <i className="fa-solid fa-file-text mr-1"></i>隐私政策
            </a>
            <a href="#" className="text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 transition-colors">
              <i className="fa-solid fa-shield mr-1"></i>安全说明
            </a>
          </div>
        </div>
        
        <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-800 text-center text-sm text-gray-500 dark:text-gray-400">
          让每一段记忆都被珍视，让每一个故事都被铭记
        </div>
      </div>
    </footer>
  );
}