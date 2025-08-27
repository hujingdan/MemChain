import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

// 预设风格数据
const presetStyles = [
  {
    id: 'oilPainting',
    name: '油画风格',
    description: '丰富的色彩和厚重的笔触质感',
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=oil%20painting%20style%20artwork&sign=3ec14b0d453b2e5bedbbe7df51b51541',
    parameters: {
      hue: 0,
      saturation: 1.2,
      brightness: { shadow: -0.1, midtone: 0.05, highlight: 0.1 },
      texture: 'oil', 
      brushSize: 'medium',
      grain: 0.2
    }
  },
  {
    id: 'watercolor',
    name: '水彩风格',
    description: '柔和的色彩过渡和透明感',
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=watercolor%20painting%20style%20artwork&sign=cacaad8fad7968bc4632c00f68b08c23',
    parameters: {
      hue: 0,
      saturation: 1.1,
      brightness: { shadow: -0.05, midtone: 0.03, highlight: 0.15 },
      texture: 'watercolor',
      brushSize: 'small',
      grain: 0.15
    }
  },
  {
    id: 'cyberpunk',
    name: '赛博朋克',
    description: '高对比度霓虹色彩和科技感',
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=cyberpunk%20style%20artwork%20neon%20colors&sign=5754fdd46a79ae16be473f2d7291ad18',
    parameters: {
      hue: 180,
      saturation: 1.5,
      brightness: { shadow: -0.2, midtone: 0.0, highlight: 0.2 },
      texture: 'digital',
      brushSize: 'large',
      grain: 0.3
    }
  },
  {
    id: 'vintage',
    name: '复古胶片',
    description: '温暖色调和颗粒感',
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=vintage%20film%20style%20photography&sign=d9837fbec3a5e25fa1321d3ac12e0180',
    parameters: {
      hue: 30,
      saturation: 1.3,
      brightness: { shadow: -0.15, midtone: 0.05, highlight: 0.05 },
      texture: 'film',
      brushSize: 'medium',
      grain: 0.4
    }
  },
  {
    id: 'minimalist',
    name: '极简主义',
    description: '简洁线条和有限色彩',
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=minimalist%20style%20artwork%20simple%20colors&sign=2a81f7f1363159500f5c184a746708a9',
    parameters: {
      hue: 0,
      saturation: 0.8,
      brightness: { shadow: -0.1, midtone: 0.1, highlight: 0.1 },
      texture: 'smooth',
      brushSize: 'small',
      grain: 0.05
    }
  }
];

// 情绪色彩映射数据
const emotionColorMaps = [
  {
    id: 'happy',
    name: '开心',
    colorScheme: { primary: '#FFB800', secondary: '#FF5722', accent: '#FF9800' },
    description: '暖黄色与橙色为主，充满活力与喜悦'
  },
  {
    id: 'calm',
    name: '平静',
    colorScheme: { primary: '#4CAF50', secondary: '#2196F3', accent: '#00BCD4' },
    description: '绿色与蓝色为主，带来宁静与放松'
  },
  {
    id: 'sad',
    name: '低落',
    colorScheme: { primary: '#9E9E9E', secondary: '#607D8B', accent: '#455A64' },
    description: '灰色与深蓝为主，表达内敛与沉思'
  },
  {
    id: 'excited',
    name: '激动',
    colorScheme: { primary: '#F44336', secondary: '#E91E63', accent: '#9C27B0' },
    description: '红色与紫色为主，展现热情与兴奋'
  },
  {
    id: 'nostalgic',
    name: '怀旧',
    colorScheme: { primary: '#795548', secondary: '#8D6E63', accent: '#A1887F' },
    description: '棕色与赭石色为主，唤起温暖回忆'
  }
];

// 可调整的参数类型定义
interface StyleParameters {
  hue: number;
  saturation: number;
  brightness: {
    shadow: number;
    midtone: number;
    highlight: number;
  };
  texture: string;
  brushSize: string;
  grain: number;
}

export default function MemoryPalette() {
  // 状态管理
  const [activeStyle, setActiveStyle] = useState<string>('');
  const [customParams, setCustomParams] = useState<StyleParameters>({
    hue: 0,
    saturation: 1,
    brightness: { shadow: 0, midtone: 0, highlight: 0 },
    texture: 'smooth',
    brushSize: 'medium',
    grain: 0.1
  });
  const [selectedEmotion, setSelectedEmotion] = useState<string>('');
  const [previewImage, setPreviewImage] = useState<string>('https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_16_9&prompt=family%20gathering%20memorable%20moment&sign=dd1d1b2837b964ab6da5a8e037ca6ee4');
  const [isCustomizing, setIsCustomizing] = useState<boolean>(false);
  const [styleHistory, setStyleHistory] = useState<StyleParameters[]>([]);
  const [historyIndex, setHistoryIndex] = useState<number>(-1);
  
  // 当选择预设风格时加载参数
  useEffect(() => {
    if (activeStyle) {
      const style = presetStyles.find(s => s.id === activeStyle);
      if (style) {
        setCustomParams(style.parameters);
        setIsCustomizing(false);
      }
    }
  }, [activeStyle]);
  
  // 当选择情绪时应用色彩映射
  useEffect(() => {
    if (selectedEmotion) {
      // 在实际应用中，这里会根据情绪色彩方案调整图像
      // 这里使用简单的滤镜效果模拟
      const emotion = emotionColorMaps.find(e => e.id === selectedEmotion);
      if (emotion) {
        // 保存当前状态到历史记录
        saveToHistory();
      }
    }
  }, [selectedEmotion]);
  
  // 保存当前样式参数到历史记录
  const saveToHistory = () => {
    const newHistory = styleHistory.slice(0, historyIndex + 1);
    newHistory.push({...customParams});
    setStyleHistory(newHistory);
    setHistoryIndex(newHistory.length - 1);
  };
  
  // 处理自定义参数变更
  const handleParamChange = (param: string, value: any, subParam?: string) => {
    if (!isCustomizing) {
      setIsCustomizing(true);
      setActiveStyle('');
    }
    
    saveToHistory();
    
    if (subParam) {
      setCustomParams(prev => ({
        ...prev,
        [param]: {
          ...prev[param as keyof StyleParameters] as object,
          [subParam]: value
        }
      }));
    } else {
      setCustomParams(prev => ({
        ...prev,
        [param]: value
      }));
    }
  };
  
  // 撤销操作
  const handleUndo = () => {
    if (historyIndex > 0) {
      setHistoryIndex(prev => prev - 1);
      setCustomParams(styleHistory[historyIndex - 1]);
    }
  };
  
  // 重做操作
  const handleRedo = () => {
    if (historyIndex < styleHistory.length - 1) {
      setHistoryIndex(prev => prev + 1);
      setCustomParams(styleHistory[historyIndex + 1]);
    }
  };
  
  // 生成预览图像的滤镜样式
  const getPreviewFilters = () => {
    const filters = [];
    
    // 色调调整
    if (customParams.hue !== 0) {
      filters.push(`hue-rotate(${customParams.hue}deg)`);
    }
    
    // 饱和度调整
    if (customParams.saturation !== 1) {
      filters.push(`saturate(${customParams.saturation})`);
    }
    
    // 亮度调整将通过CSS变量在图像容器中应用
    
    return filters.join(' ');
  };
  
  // 获取纹理背景样式
  const getTextureBackground = () => {
    switch (customParams.texture) {
      case 'oil':
        return 'url(https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=oil%20painting%20texture&sign=fcb4c304be2ec9d5b0e818ce05fc4517)';
      case 'watercolor':
        return 'url(https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=watercolor%20paper%20texture&sign=e1d12f0672680349afe78a6f7f943a44)';
      case 'film':
        return 'url(https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=film%20grain%20texture&sign=d4e0a06e5664bfeb9bc83cc2678a92d8)';
      case 'digital':
        return 'url(https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=digital%20noise%20texture&sign=b9fb0d5d1ab9256e78dc60dd2f904be2)';
      default:
        return 'none';
    }
  };
  
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 text-gray-900 dark:text-gray-100">
      {/* 导航栏 */}
      <Navbar />
      
      <div className="container mx-auto px-4 py-8">
        {/* 页面标题 */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-500 to-orange-600 dark:from-amber-400 dark:to-orange-500 mb-2">
            记忆调色盘
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            用色彩与风格，重新定义您的珍贵记忆
          </p>
        </div>
        
        {/* 主内容区 - 响应式布局 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* 左侧：风格选择面板 */}
          <div className="lg:col-span-1 space-y-8">
            {/* 预设风格库 */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
              <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-gray-200">预设风格库</h2>
              <div className="space-y-4">
                {presetStyles.map(style => (
                  <motion.div
                    key={style.id}
                    onClick={() => setActiveStyle(style.id)}
                    className={cn(
                      "flex items-center p-3 rounded-xl border transition-all cursor-pointer group",
                      activeStyle === style.id && !isCustomizing
                        ? "border-amber-500 bg-amber-50 dark:bg-amber-900/20 shadow-md"
                        : "border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-750"
                    )}
                    whileHover={{ x: 5 }}
                  >
                    <div className="w-20 h-20 rounded-lg overflow-hidden flex-shrink-0">
                      <img 
                        src={style.thumbnail} 
                        alt={style.name}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="ml-4 flex-grow">
                      <h3 className="font-medium text-gray-900 dark:text-white">{style.name}</h3>
                      <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2">{style.description}</p>
                    </div>
                    {activeStyle === style.id && !isCustomizing && (
                      <i className="fa-solid fa-check text-amber-500 ml-2"></i>
                    )}
                  </motion.div>
                ))}
              </div>
            </div>
            
            {/* 情绪色彩映射 */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
              <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-gray-200">情绪色彩映射</h2>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">选择情绪，自动匹配色彩方案</p>
              
              <div className="grid grid-cols-2 gap-3">
                {emotionColorMaps.map(emotion => (
                  <button
                    key={emotion.id}
                    onClick={() => setSelectedEmotion(emotion.id === selectedEmotion ? '' : emotion.id)}
                    className={cn(
                      "p-3 rounded-xl text-left transition-all border",
                      selectedEmotion === emotion.id
                        ? "border-amber-500 bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/20 shadow-md"
                        : "border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-750"
                    )}
                  >
                    <div className="flex items-center mb-1">
                      <div className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: emotion.colorScheme.primary }}></div>
                      <h3 className="font-medium text-gray-900 dark:text-white text-sm">{emotion.name}</h3>
                    </div>
                    <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2">{emotion.description}</p>
                  </button>
                ))}
              </div>
            </div>
          </div>
          
          {/* 右侧：效果预览区 + 自定义工具 */}
          <div className="lg:col-span-2 space-y-8">
            {/* 效果预览区 */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-xl font-bold text-gray-800 dark:text-gray-200">效果预览</h2>
                <p className="text-sm text-gray-600 dark:text-gray-400">实时查看风格调整效果</p>
              </div>
              
              <div className="relative p-6 flex justify-center items-center min-h-[400px] bg-gray-100 dark:bg-gray-900">
                {/* 预览图像容器 - 应用亮度和对比度调整 */}
                <div 
                  className="relative w-full max-w-lg aspect-[4/3] rounded-xl overflow-hidden shadow-inner"
                  style={{
                    '--shadow-brightness': customParams.brightness.shadow,
                    '--midtone-brightness': customParams.brightness.midtone,
                    '--highlight-brightness': customParams.brightness.highlight,
                    filter: 'contrast(1.1)'
                  }}
                >
                  {/* 主图像 - 应用色调和饱和度调整 */}
                  <img 
                    src={previewImage} 
                    alt="风格预览"
                    className="absolute inset-0 w-full h-full object-cover transition-all duration-500"
                    style={{
                      filter: getPreviewFilters(),
                      mixBlendMode: 'normal'
                    }}
                  />
                  
                  {/* 纹理叠加层 */}
                  {customParams.texture !== 'smooth' && (
                    <div 
                      className="absolute inset-0 opacity-15 mix-blend-overlay"
                      style={{
                        backgroundImage: getTextureBackground(),
                        backgroundSize: 'cover',
                        backgroundBlendMode: 'multiply'
                      }}
                    />
                  )}
                  
                  {/* 颗粒效果 */}
                  {customParams.grain > 0 && (
                    <div 
                      className="absolute inset-0 pointer-events-none"
                      style={{
                        backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency=${customParams.grain} numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
                        opacity: 0.15,
                        mixBlendMode: 'overlay'
                      }}
                    />
                  )}
                  
                  {/* 情绪色彩覆盖层（如果选择了情绪） */}
                  {selectedEmotion && (
                    <div 
                      className="absolute inset-0 opacity-10 mix-blend-color"
                      style={{
                        backgroundColor: emotionColorMaps.find(e => e.id === selectedEmotion)?.colorScheme.primary
                      }}
                    />
                  )}
                </div>
                
                {/* 加载状态指示器（模拟处理中效果） */}
                <AnimatePresence>
                  {/* 这里可以添加加载动画 */}
                </AnimatePresence>
              </div>
              
              {/* 操作按钮 */}
              <div className="p-4 bg-gray-50 dark:bg-gray-850 flex justify-between items-center border-t border-gray-200 dark:border-gray-700">
                <div className="flex space-x-2">
                  <button 
                    onClick={handleUndo}
                    disabled={historyIndex <= 0}
                    className="p-2 rounded-full text-gray-600 dark:text-gray-400 hover:text-amber-500 dark:hover:text-amber-400 disabled:opacity-50 disabled:cursor-not-allowed"
                    title="撤销"
                  >
                    <i className="fa-solid fa-undo"></i>
                  </button>
                  <button 
                    onClick={handleRedo}
                    disabled={historyIndex >= styleHistory.length - 1}
                    className="p-2 rounded-full text-gray-600 dark:text-gray-400 hover:text-amber-500 dark:hover:text-amber-400 disabled:opacity-50 disabled:cursor-not-allowed"
                    title="重做"
                  >
                    <i className="fa-solid fa-redo"></i>
                  </button>
                </div>
                
                <div className="flex space-x-3">
                  <button className="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-full text-sm font-medium transition-colors flex items-center">
                    <i className="fa-solid fa-download mr-2"></i>
                    更换图片
                  </button>
                  <button className="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white rounded-full text-sm font-medium transition-colors flex items-center">
                    <i className="fa-solid fa-magic mr-2"></i>
                    应用效果
                  </button>
                </div>
              </div>
            </div>
            
            {/* 自定义风格工具 */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
              <h2 className="text-xl font-bold mb-6 text-gray-800 dark:text-gray-200">自定义风格工具</h2>
              
              <div className="space-y-8">
                {/* 色调和饱和度调整 */}
                <div>
                  <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">色调与饱和度</h3>
                  
                  <div className="space-y-6">
                    {/* 色调调整 */}
                    <div>
                      <div className="flex justify-between mb-2">
                        <label className="text-xs text-gray-600 dark:text-gray-400">色调</label>
                        <span className="text-xs font-medium text-gray-900 dark:text-white">{customParams.hue}°</span>
                      </div>
                      <input
                        type="range"
                        min="-180"
                        max="180"
                        step="1"
                        value={customParams.hue}
                        onChange={(e) => handleParamChange('hue', parseInt(e.target.value))} 
                        className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-amber-500"
                      />
                      <div className="flex justify-between text-xs text-gray-500 dark:text-gray-500 mt-1">
                        <span>-180°</span>
                        <span>0°</span>
                        <span>+180°</span>
                      </div>
                    </div>
                    
                    {/* 饱和度调整 */}
                    <div>
                      <div className="flex justify-between mb-2">
                        <label className="text-xs text-gray-600 dark:text-gray-400">饱和度</label>
                        <span className="text-xs font-medium text-gray-900 dark:text-white">{customParams.saturation.toFixed(1)}x</span>
                      </div>
                      <input
                        type="range"
                        min="0.5"
                        max="2"
                        step="0.1"
                        value={customParams.saturation}
                        onChange={(e) => handleParamChange('saturation', parseFloat(e.target.value))} 
                        className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-amber-500"
                      />
                      <div className="flex justify-between text-xs text-gray-500 dark:text-gray-500 mt-1">
                        <span>0.5x</span>
                        <span>1.0x</span> 
                        <span>2.0x</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                {/* 亮度调整 */}
                <div>
                  <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">亮度调整</h3>
                  
                  <div className="space-y-6">
                    {/* 阴影亮度 */}
                    <div>
                      <div className="flex justify-between mb-2">
                        <label className="text-xs text-gray-600 dark:text-gray-400">阴影</label>
                        <span className="text-xs font-medium text-gray-900 dark:text-white">{(customParams.brightness.shadow * 100).toFixed(0)}%</span>
                      </div>
                      <input
                        type="range"
                        min="-0.5"
                        max="0.5" 
                        step="0.05" 
                        value={customParams.brightness.shadow}
                        onChange={(e) => handleParamChange('brightness', parseFloat(e.target.value), 'shadow')} 
                        className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-amber-500"
                      />
                    </div>
                    
                    {/* 中间调亮度 */}
                    <div>
                      <div className="flex justify-between mb-2">
                        <label className="text-xs text-gray-600 dark:text-gray-400">中间调</label>
                        <span className="text-xs font-medium text-gray-900 dark:text-white">{(customParams.brightness.midtone * 100).toFixed(0)}%</span>
                      </div> 
                      <input
                        type="range"
                        min="-0.5"
                        max="0.5"
                        step="0.05"
                        value={customParams.brightness.midtone}
                        onChange={(e) => handleParamChange('brightness', parseFloat(e.target.value), 'midtone')} 
                        className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-amber-500"
                      />
                    </div>
                    
                    {/* 高光亮度 */}
                    <div>
                      <div className="flex justify-between mb-2"> 
                        <label className="text-xs text-gray-600 dark:text-gray-400">高光</label>
                        <span className="text-xs font-medium text-gray-900 dark:text-white">{(customParams.brightness.highlight * 100).toFixed(0)}%</span>
                      </div>
                      <input
                        type="range"
                        min="-0.5"
                        max="0.5"
                        step="0.05"
                        value={customParams.brightness.highlight}
                        onChange={(e) => handleParamChange('brightness', parseFloat(e.target.value), 'highlight')} 
                        className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-amber-500"
                      />
                    </div>
                  </div>
                </div>
                
                {/* 纹理和颗粒调整 */}
                <div>
                  <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">纹理与质感</h3>
                  
                  <div className="grid grid-cols-2 gap-4">
                    {/* 纹理类型选择 */}
                    <div>
                      <label className="text-xs text-gray-600 dark:text-gray-400 block mb-2">纹理类型</label>
                      <select
                        value={customParams.texture}
                        onChange={(e) => handleParamChange('texture', e.target.value)}
                        className="w-full px-3 py-2 bg-gray-100 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
                      >
                        <option value="smooth">无纹理</option>
                        <option value="oil">油画纹理</option>
                        <option value="watercolor">水彩纹理</option>
                        <option value="film">胶片纹理</option>
                        <option value="digital">数字纹理</option>
                      </select>
                    </div>
                    
                    {/* 笔触大小 */}
                    <div>
                      <label className="text-xs text-gray-600 dark:text-gray-400 block mb-2">笔触大小</label>
                      <select
                        value={customParams.brushSize}
                        onChange={(e) => handleParamChange('brushSize', e.target.value)}
                        className="w-full px-3 py-2 bg-gray-100 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
                      >
                        <option value="small">小笔触</option>
                        <option value="medium">中等笔触</option>
                        <option value="large">大笔触</option>
                      </select>
                    </div>
                  </div>
                  
                  {/* 颗粒感调整 */}
                  <div className="mt-6">
                    <div className="flex justify-between mb-2">
                      <label className="text-xs text-gray-600 dark:text-gray-400">颗粒感</label>
                      <span className="text-xs font-medium text-gray-900 dark:text-white">{(customParams.grain * 100).toFixed(0)}%</span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="0.5"
                      step="0.01"
                      value={customParams.grain} 
                      onChange={(e) => handleParamChange('grain', parseFloat(e.target.value))} 
                      className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-amber-500"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* 页脚 */}
      <Footer />
    </div>
  );
}