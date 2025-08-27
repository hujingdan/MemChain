import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { cn } from '@/lib/utils';

// Mock data for theme cards in museum entrance wall
const themeCards = [
  {
    id: 'family',
    title: '家庭时光',
    description: '记录与家人共度的温馨时刻',
    coverImage: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=family%20memories%20photo%20album%20warm%20colors&sign=dbccd6c8d86d293b6aab809e74277df9',
    memoriesCount: 24,
    yearRange: '2018-2024',
    colorScheme: { primary: '#FF6B6B', secondary: '#FFD166' }
  },
  {
    id: 'travel',
    title: '旅途足迹',
    description: '探索世界各地的美好回忆',
    coverImage: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=travel%20photography%20collection%20vibrant%20colors&sign=2750a13ee27a307bf01a5d9334d80027',
    memoriesCount: 37,
    yearRange: '2019-2023',
    colorScheme: { primary: '#06D6A0', secondary: '#118AB2' }
  },
  {
    id: 'career',
    title: '职场成长',
    description: '记录职业生涯的重要里程碑',
    coverImage: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=career%20achievements%20professional%20milestones&sign=9183010b373a946da24075ed9bc0d3fe',
    memoriesCount: 18,
    yearRange: '2020-2024',
    colorScheme: { primary: '#118AB2', secondary: '#073B4C' }
  },
  {
    id: 'hobbies',
    title: '兴趣爱好',
    description: '记录那些让生活更精彩的爱好',
    coverImage: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=hobbies%20collection%20painting%20music%20sports&sign=0296a62b203e5f4d69a0073c34074462',
    memoriesCount: 29,
    yearRange: '2017-2024',
    colorScheme: { primary: '#9381FF', secondary: '#B8B8FF' }
  },
  {
    id: 'friends',
    title: '友谊长存',
    description: '与朋友们共度的欢乐时光',
    coverImage: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=friends%20gathering%20happy%20moments%20laughter&sign=3ee0a39160cf8b195d1778edbae98241',
    memoriesCount: 22,
    yearRange: '2016-2024',
    colorScheme: { primary: '#FFD166', secondary: '#06D6A0' }
  },
  {
    id: 'seasons',
    title: '四季更迭',
    description: '记录不同季节的美丽景色',
    coverImage: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=four%20seasons%20landscape%20changing%20nature&sign=0151dd561cf981257220f66d9585fb1c',
    memoriesCount: 15,
    yearRange: '2021-2023',
    colorScheme: { primary: '#00BBF9', secondary: '#F15BB5' }
  }
];

// Mock data for immersive space content
const immersiveContent = {
  photos: [
    {
      id: 1,
      url: 'https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_4_3&prompt=family%20dinner%20warm%20lighting&sign=57a54203a805ee4ff8dd8de9b39dfc6c',
      year: 2022,
      description: '春节家庭聚餐'
    },
    {
      id: 2,
      url: 'https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_4_3&prompt=beach%20vacation%20tropical%20paradise&sign=8e2d71bdfe778137b88a5eb598141805',
      year: 2021,
      description: '巴厘岛海滩度假'
    },
    {
      id: 3,
      url: 'https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_4_3&prompt=graduation%20ceremony%20proud%20moment&sign=1d893efd5a3cefe0d84fe83a4c12ecef',
      year: 2020,
      description: '大学毕业典礼'
    },
    {
      id: 4,
      url: 'https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_4_3&prompt=birthday%20celebration%20cake%20candles&sign=81270733dcddaca0a38928d72da364cb',
      year: 2023,
      description: '25岁生日'
    },
    {
      id: 5,
      url: 'https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_4_3&prompt=first%20apartment%20new%20home&sign=73c29c291ed21c76b0f7318ab1094800',
      year: 2022,
      description: '第一个属于自己的公寓'
    },
    {
      id: 6,
      url: 'https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_4_3&prompt=mountains%20hiking%20adventure%20view&sign=3ee9897d822c69650d59b8da2acaf1fc',
      year: 2021,
      description: '黄山徒步旅行'
    }
  ],
  notes: [
    {
      id: 1,
      title: '旅行日记 - 西藏',
      excerpt: '站在布达拉宫前，我感受到了前所未有的震撼...',
      date: '2021-08-15',
      coverImage: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=travel%20journal%20tibet%20landscape&sign=b16b861752014d405052a399b109a850'
    },
    {
      id: 2,
      title: '工作感悟 - 晋升',
      excerpt: '今天收到了晋升通知，三年的努力终于有了回报...',
      date: '2022-11-03',
      coverImage: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=work%20achievement%20celebration&sign=77093cbc22966be821d834c1ff4c0d6a'
    },
    {
      id: 3,
      title: '读书笔记 - 活着',
      excerpt: '余华的《活着》让我重新思考了生命的意义...',
      date: '2023-04-22',
      coverImage: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=book%20notes%20literature%20reflection&sign=bab419d483cb4aeb3fcdf49dc0b3691f'
    }
  ]
};

// Mock timeline data
const timelineData = [
  { year: 2018, events: 3, description: '开始记录生活' },
  { year: 2019, events: 5, description: '第一次独自旅行' },
  { year: 2020, events: 8, description: '大学毕业，步入职场' },
  { year: 2021, events: 12, description: '环球旅行计划启动' },
  { year: 2022, events: 15, description: '晋升为部门主管' },
  { year: 2023, events: 10, description: '出版第一本书' },
  { year: 2024, events: 7, description: '新的生活阶段' }
];

export default function ThemeMuseum() {
  const [activeSection, setActiveSection] = useState<'entrance' | 'immersive' | 'timeline'>('entrance');
  const [selectedTheme, setSelectedTheme] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeYear, setActiveYear] = useState<number>(2020);

  // Simulate loading
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1000);
    
    return () => clearTimeout(timer);
  }, []);

  // Handle theme selection
  const handleThemeSelect = (themeId: string) => {
    setSelectedTheme(themeId);
    setActiveSection('immersive');
    
    // Scroll to immersive section
    setTimeout(() => {
      const element = document.getElementById('immersive-space');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }, 300);
  };

  // Get theme details by ID
  const getSelectedTheme = () => {
    if (!selectedTheme) return themeCards[0];
    return themeCards.find(theme => theme.id === selectedTheme) || themeCards[0];
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 text-gray-900 dark:text-gray-100">
      {/* Navigation */}
      <Navbar />
      
      {/* Loading state */}
      {isLoading && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-white/80 dark:bg-gray-900/80 backdrop-blur-md">
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 border-t-4 border-b-4 border-amber-500 rounded-full animate-spin mb-4"></div>
            <h3 className="text-xl font-medium text-gray-800 dark:text-gray-200">正在加载主题博物馆...</h3>
          </div>
        </div>
      )}
      
      <div className="container mx-auto px-4 py-8">
        {/* Page title */}
        <div className="mb-12 text-center">
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-500 to-rose-600 dark:from-amber-400 dark:to-rose-500 mb-4">
            主题博物馆
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            漫步于记忆的殿堂，探索那些珍贵的主题收藏
          </p>
        </div>
        
        {/* Museum entrance wall - Theme cards */}
        <section id="entrance-wall" className="mb-20">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 md:p-8">
            <h2 className="text-2xl font-bold mb-8 text-gray-800 dark:text-gray-200 flex items-center">
              <i className="fa-solid fa-university text-amber-500 mr-3"></i>
              博物馆入口墙
            </h2>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {themeCards.map((theme, index) => (
                <motion.div
                  key={theme.id}
                  onClick={() => handleThemeSelect(theme.id)}
                  className="group rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700 shadow-md hover:shadow-xl transition-all duration-300 cursor-pointer"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }} 
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ y: -8 }}
                >
                  <div className="relative h-48 overflow-hidden">
                    <img 
                      src={theme.coverImage} 
                      alt={theme.title}
                      className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent"></div>
                    <div className="absolute bottom-0 left-0 right-0 p-4">
                      <h3 className="text-xl font-bold text-white mb-1">{theme.title}</h3>
                      <p className="text-sm text-gray-200 line-clamp-2">{theme.description}</p>
                    </div>
                    <div className="absolute top-3 right-3 bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm rounded-full px-3 py-1 text-xs font-medium text-gray-800 dark:text-gray-200">
                      {theme.memoriesCount} 个记忆
                    </div>
                  </div>
                  <div className="p-4 bg-gray-50 dark:bg-gray-850 flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">{theme.yearRange}</span>
                    <button className="text-amber-500 hover:text-amber-600 dark:text-amber-400 dark:hover:text-amber-300 font-medium text-sm flex items-center group/button">
                      进入展厅
                      <i className="fa-solid fa-arrow-right ml-1 transition-transform group-hover/button:translate-x-1"></i>
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>
        
        {/* Immersive space */}
        <section id="immersive-space" className="mb-20">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
            {/* Theme header */}
            <div className="p-6 md:p-8 bg-gradient-to-r from-amber-500 to-rose-600 text-white">
              <div className="flex justify-between items-center">
                <div>
                  <h2 className="text-2xl font-bold flex items-center">
                    <i className="fa-solid fa-vr-cardboard mr-3"></i>
                    {getSelectedTheme().title} 主题展厅
                  </h2>
                  <p className="mt-1 opacity-90">{getSelectedTheme().description}</p>
                </div>
                <button 
                  onClick={() => setActiveSection('entrance')}
                  className="bg-white/20 hover:bg-white/30 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-medium transition-colors flex items-center"
                >
                  <i className="fa-solid fa-arrow-left mr-2"></i>
                  返回主题墙
                </button>
              </div>
            </div>
            
            {/* Immersive content area */}
            <div className="p-6 md:p-8">
              {/* Photo wall */}
              <div className="mb-12">
                <h3 className="text-xl font-bold mb-6 text-gray-800 dark:text-gray-200 flex items-center">
                  <i className="fa-solid fa-images text-amber-500 mr-2"></i>
                  照片墙
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                  {immersiveContent.photos.map((photo, index) => (
                    <motion.div 
                      key={photo.id}
                      className="group relative rounded-xl overflow-hidden aspect-square cursor-pointer"
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: index * 0.05 }}
                    >
                      <img 
                        src={photo.url} 
                        alt={photo.description}
                        className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-3">
                        <h4 className="text-white font-medium text-sm">{photo.description}</h4>
                        <p className="text-gray-200 text-xs">{photo.year}年</p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
              
              {/* Notes display case */}
              <div>
                <h3 className="text-xl font-bold mb-6 text-gray-800 dark:text-gray-200 flex items-center">
                  <i className="fa-solid fa-book-open text-amber-500 mr-2"></i>
                  笔记展柜
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {immersiveContent.notes.map((note, index) => (
                    <motion.div 
                      key={note.id}
                      className="bg-gray-50 dark:bg-gray-850 rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-all duration-300"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <div className="h-36 overflow-hidden">
                        <img 
                          src={note.coverImage} 
                          alt={note.title}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div className="p-4">
                        <h4 className="font-bold text-gray-900 dark:text-white mb-2">{note.title}</h4>
                        <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-3 mb-4">{note.excerpt}</p>
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-gray-500 dark:text-gray-500">{note.date}</span>
                          <button className="text-amber-500 hover:text-amber-600 dark:text-amber-400 dark:hover:text-amber-300 text-sm font-medium">
                            阅读全文
                          </button>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>
        
        {/* Timeline navigation */}
        <section id="timeline-navigation">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 md:p-8">
            <h2 className="text-2xl font-bold mb-8 text-gray-800 dark:text-gray-200 flex items-center">
              <i className="fa-solid fa-history text-amber-500 mr-3"></i>
              时间轴导航
            </h2>
            
            <div className="relative">
              {/* Timeline line */}
              <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-gray-300 dark:bg-gray-700 transform -translate-x-1/2"></div>
              
              <div className="space-y-16 relative z-10">
                {timelineData.map((yearData, index) => (
                  <div 
                    key={yearData.year}
                    className="flex items-center" 
                  >
                    <div className={`w-full ${index % 2 === 0 ? 'pr-12 text-right' : 'pl-12'}`}>
                      <motion.button
                        onClick={() => setActiveYear(yearData.year)}
                        className={cn(
                          "inline-block px-6 py-3 rounded-xl transition-all",
                          activeYear === yearData.year
                            ? "bg-amber-500 text-white shadow-lg shadow-amber-500/20"
                            : "bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600"
                        )}
                        whileHover={{ scale: 1.05 }}
                      >
                        <span className="text-xl font-bold">{yearData.year}</span>
                        <span className="ml-2 text-sm opacity-80">({yearData.events} 个事件)</span>
                      </motion.button>
                      {activeYear === yearData.year && (
                        <p className="mt-3 text-gray-600 dark:text-gray-400 inline-block text-sm max-w-xs">
                          {yearData.description}
                        </p>
                      )}
                    </div>
                    <div className="absolute left-1/2 w-6 h-6 rounded-full bg-amber-500 transform -translate-x-1/2 border-4 border-white dark:border-gray-800"></div>
                    <div className="w-full"></div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="mt-12 text-center">
              <p className="text-gray-600 dark:text-gray-400 mb-4">沿着时间线，探索您人生中的重要时刻</p>
              <button className="px-6 py-3 bg-amber-500 hover:bg-amber-600 text-white rounded-full font-medium shadow-md hover:shadow-lg transition-all flex items-center mx-auto">
                <i className="fa-solid fa-compass mr-2"></i>
                开始时间旅行
              </button>
            </div>
          </div>
        </section>
      </div>
      
      {/* Footer */}
      <Footer />
    </div>
  );
}