import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { useTheme } from '@/hooks/useTheme';

// 导航栏组件
export default function Navbar() {
  const { theme, toggleTheme } = useTheme();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  // 导航项数据
  const navItems = [
    { path: '/', label: '首页' },
    { path: '/aicurator', label: 'AI策展' },
    { path: '/timestream', label: '时光流' },
      { path: '/memorypalette', label: '记忆调色盘' },
      { path: '/privatediary', label: '私密日记' },
     { path: '/thememuseum', label: '主题博物馆' },
    { path: '/other', label: '数据管理' },
    { path: '/other', label: '记忆空间' },
    { path: '/other', label: '设置' },
  ];
  
  return (
    <nav className="sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-800">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <i className="fa-solid fa-link text-2xl text-blue-600 dark:text-blue-400 mr-2"></i>
            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-700 dark:from-blue-400 dark:to-indigo-500">MemChain</span>
          </div>
          
           {/* 桌面导航 */}
           <div className="hidden md:flex items-center space-x-6">
              {navItems.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) => 
                    isActive 
                      ? "text-blue-600 dark:text-blue-400 font-medium" 
                      : "text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                  }
                >
                  {item.label}
                </NavLink>
              ))}
          </div>
          
          {/* 右侧功能区 */}
          <div className="flex items-center space-x-4">
            {/* 主题切换按钮 */}
            <button 
              onClick={toggleTheme}
              className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
              aria-label={theme === 'light' ? '切换到深色模式' : '切换到浅色模式'}
            >
              {theme === 'light' ? (
                <i className="fa-solid fa-moon text-gray-700"></i>
              ) : (
                <i className="fa-solid fa-sun text-yellow-400"></i>
              )}
            </button>
            
            {/* 用户头像 */}
            <div className="relative">
              <button className="w-10 h-10 rounded-full bg-gradient-to-r from-purple-400 to-pink-500 flex items-center justify-center text-white font-medium">
                <i className="fa-solid fa-user"></i>
              </button>
            </div>
            
            {/* 移动端菜单按钮 */}
            <button 
              className="md:hidden p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              aria-label="菜单"
            >
              {isMenuOpen ? (
                <i className="fa-solid fa-x"></i>
              ) : (
                <i className="fa-solid fa-bars"></i>
              )}
            </button>
          </div>
        </div>
      </div>
      
      {/* 移动端导航菜单 */}
      {isMenuOpen && (
        <div className="md:hidden bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
           <div className="px-4 py-3 space-y-3">
              {navItems.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) => 
                    isActive 
                      ? "block py-2 text-blue-600 dark:text-blue-400 font-medium" 
                      : "block py-2 text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400"
                  }
                  onClick={() => setIsMenuOpen(false)}
                >
                  {item.label}
                </NavLink>
              ))}
           </div>
        </div>
      )}
    </nav>
  );
}