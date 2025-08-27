import { useState, useEffect } from 'react';
import Navbar from '@/components/Navbar';
import FeatureCard from '@/components/FeatureCard';
import DataOverview from '@/components/DataOverview';
import SecurityPrompt from '@/components/SecurityPrompt';
import Footer from '@/components/Footer';
import { motion } from 'framer-motion';

// 模拟用户数据统计
const userData = {
  photos: 120,
  recordings: 30,
  notes: 50,
};

// MemChain首页组件
export default function Home() {
  const [isLoading, setIsLoading] = useState(true);
  
  // 添加页面加载动画效果
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, );
    
    return () => clearTimeout(timer);
  }, []);
  
  // 核心功能数据
  const features = [
    {
      title: "时光流",
      description: "智能时间线，串联您的人生记忆",
      icon: "fa-clock-rotate-left",
      color: "from-blue-500 to-indigo-600",
      imageUrl: "https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_16_9&prompt=timeline%20of%20memories%20with%20photos%20and%20events&sign=ee5db63b47554c129abfae50b7a24134",
      path: "/timestream"
    },
     {
      title: "AI策展助理",
      description: "智能生成专属回忆展览方案",
      icon: "fa-magic",
      color: "from-purple-500 to-pink-600",
      imageUrl: "https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_16_9&prompt=AI%20curator%20exhibition%20design%20interface&sign=cc9c6fcdffcf0ee7a8493f21d3381143",
      path: "/aicurator"
    },
     {
      title: "记忆调色盘",
      description: "艺术化风格处理，定制记忆色彩",
      icon: "fa-palette",
      color: "from-amber-500 to-orange-600",
      imageUrl: "https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_16_9&prompt=color%20palette%20with%20artistic%20photo%20filters&sign=d44ecec3ff0a40b49a25a7ff8787d6ea",
      path: "/memorypalette"
    },
    {
      title: "主题博物馆",
      description: "创建专属主题空间，沉浸式回忆体验",
      icon: "fa-university",
      color: "from-emerald-500 to-teal-600",
      imageUrl: "https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_16_9&prompt=museum%20exhibition%20hall%20with%20memories%20display&sign=f31ea305efad952dd521729f4d9b9add"
    },
    {
      title: "私密日记助手",
      description: "本地处理，安全记录您的内心世界",
      icon: "fa-book-open",
      color: "from-rose-500 to-red-600",
      imageUrl: "https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_16_9&prompt=private%20diary%20with%20lock%20and%20security%20features&sign=f35383f68c20cb3d178c854afa93806e"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 text-gray-900 dark:text-gray-100">
      {/* 导航栏 */}
      <Navbar />
      
      {/* 加载状态 */}
      {isLoading ? (
        <div className="flex items-center justify-center min-h-[80vh]">
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 border-4 border-t-blue-500 border-gray-200 dark:border-gray-700 rounded-full animate-spin mb-4"></div>
            <p className="text-lg font-medium text-gray-600 dark:text-gray-400">正在加载您的人生博物馆...</p>
          </div>
        </div>
      ) : (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="container mx-auto px-4 py-8"
        >
          {/* 英雄区域 */}
          <section className="text-center mb-16 mt-8">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-700 dark:from-blue-400 dark:to-indigo-500">
              MemChain
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
              珍藏每一段时光，做自己故事的观众
            </p>
            <div className="inline-block px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-700 rounded-full text-white font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300">
              <i className="fa-solid fa-upload mr-2"></i>开始收集您的记忆
            </div>
          </section>
          
          {/* 数据概览 */}
          <DataOverview data={userData} />
          
          {/* 核心功能区域 */}
          <section className="mb-16">
            <h2 className="text-3xl font-bold text-center mb-12 text-gray-800 dark:text-gray-200">
              探索您的记忆世界
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {features.map((feature, index) => (
                <FeatureCard key={index} {...feature} />
              ))}
            </div>
          </section>
          
          {/* 安全提示 */}
          <SecurityPrompt />
        </motion.div>
      )}
      
      {/* 页脚 */}
      <Footer />
    </div>
  );
}