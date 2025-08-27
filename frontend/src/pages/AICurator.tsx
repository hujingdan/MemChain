import { useState } from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

// 模拟素材数据
const mockMaterials = [
  {
    id: 1,
    type: 'photo',
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=family%20dinner%20photo%20warm%20lighting&sign=c904e2981f3d492923391bf2146b0612',
    date: '2023-10-01'
  },
  { id: '2', type: 'photo', thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=birthday%20celebration%20candle%20cake&sign=3da0cde270322cbfa5c110f56d36f452', date: '2023-10-02' },
  { id: '3', type: 'recording', thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=audio%20waveform%20visualization%20blue&sign=84181560d83f378bb1b613b82073ba4d', date: '2023-10-03' },
  { id: '4', type: 'photo', thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=sunset%20over%20mountain%20landscape&sign=8338e0ea0df8a87f8569f87f00eb4c26', date: '2023-10-05' },
  { id: '5', type: 'note', thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=handwritten%20note%20paper%20texture&sign=c3dee662709b7a0c3418a1ed84af4e70', date: '2023-10-07' },
  { id: '6', type: 'photo', thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=friends%20gathering%20laughter%20outdoor&sign=72cb1c0eeb15b2679665441e9a76c968', date: '2023-10-10' },
];

// 可视化形式推荐数据
const visualizationOptions = [
  {
    id: 'album',
    name: '互动电子相册',
    description: '可翻页的互动式相册，支持添加文字说明和背景音乐',
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_4_3&prompt=interactive%20photo%20album%20digital%20interface&sign=f9f1d3a669e0988bf50aa1f6ee3f0640'
  },
  {
    id: 'video',
    name: '动态短视频',
    description: '自动生成带转场效果的短视频，可添加背景音乐和文字字幕',
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_4_3&prompt=video%20editing%20interface%20timeline%20preview&sign=081838c1da4d8095713bfecc1d39e653'
  },
  {
    id: 'storyboard',
    name: '图文故事板',
    description: '图文结合的故事展示形式，适合讲述有时间线的完整故事',
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=landscape_4_3&prompt=storyboard%20layout%20with%20images%20and%20text&sign=25d3bd486582623f06752c7c5f06b710'
  }
];

// 情绪选项
const emotionOptions = [
  { id: 'warm', name: '温馨', color: 'from-amber-400 to-orange-500' },
  { id: 'cheerful', name: '欢快', color: 'from-yellow-400 to-amber-500' },
  { id: 'calm', name: '平静', color: 'from-blue-400 to-cyan-500' },
  { id: 'nostalgic', name: '怀旧', color: 'from-purple-400 to-pink-500' },
  { id: 'inspiring', name: '励志', color: 'from-green-400 to-teal-500' },
];

// 风格选项
const styleOptions = [
  { id: 'minimalist', name: '极简风', description: '简洁干净的设计，突出内容本身' },
  { id: 'vintage', name: '复古风', description: '带有年代感的色调和纹理' },
  { id: 'cartoon', name: '卡通风', description: '可爱的卡通化视觉效果' },
  { id: 'cinematic', name: '电影感', description: '宽屏比例和电影色调处理' },
  { id: 'watercolor', name: '水彩风', description: '柔和的水彩画效果' },
];

export default function AICurator() {
  // 状态管理
  const [activeStep, setActiveStep] = useState<'input' | 'results'>('input');
  const [selectedEmotion, setSelectedEmotion] = useState<string>('');
  const [selectedStyle, setSelectedStyle] = useState<string>('');
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [selectedVisualization, setSelectedVisualization] = useState<string>('album');
  
  // 表单状态
  const [formData, setFormData] = useState({
    theme: '',
    startDate: '',
    endDate: '',
  });
  
  // 处理表单输入变化
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };
  
  // 处理生成策展方案
  const handleGeneratePlan = () => {
    if (!formData.theme || !formData.startDate || !formData.endDate || !selectedEmotion || !selectedStyle) {
      alert('请填写所有必填字段');
      return;
    }
    
    setIsGenerating(true);
    
    // 模拟AI生成过程
    setTimeout(() => {
      setIsGenerating(false);
      setActiveStep('results');
    }, 2000);
  };
  
  // 处理返回修改
  const handleBackToEdit = () => {
    setActiveStep('input');
  };
  
  // 处理生成最终作品
  const handleGenerateFinal = () => {
    alert('最终作品生成中，这将调用AI处理并创建您的专属记忆策展...');
  };
  
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 text-gray-900 dark:text-gray-100">
      {/* 导航栏 */}
      <Navbar />
      
      <div className="container mx-auto px-4 py-8">
        {/* 页面标题 */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-pink-600 dark:from-purple-400 dark:to-pink-400 mb-2">
            AI策展助理
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            智能生成专属回忆展览方案，让您的珍贵记忆焕发新生
          </p>
        </div>
        
        {/* 步骤指示器 */}
        <div className="mb-10">
          <div className="flex items-center justify-between max-w-2xl mx-auto">
            <div className="flex flex-col items-center">
              <div className={`w-12 h-12 rounded-full flex items-center justify-center font-bold ${activeStep === 'input' ? 'bg-purple-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400'}`}>
                1
              </div>
              <span className="mt-2 text-sm font-medium">输入需求</span>
            </div>
            
            <div className="flex-1 h-1 mx-4 bg-gradient-to-r from-purple-600 to-pink-600"></div>
            
            <div className="flex flex-col items-center">
              <div className={`w-12 h-12 rounded-full flex items-center justify-center font-bold ${activeStep === 'results' ? 'bg-pink-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400'}`}>
                2
              </div>
              <span className="mt-2 text-sm font-medium">策展方案</span>
            </div>
          </div>
        </div>
        
        {/* 需求输入区 */}
        {activeStep === 'input' && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 md:p-8 mb-10"
          >
            <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-200">告诉AI您的策展需求</h2>
            
            <div className="space-y-6">
              {/* 主题输入 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  策展主题 <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  name="theme"
                  value={formData.theme}
                  onChange={handleInputChange}
                  placeholder="例如：2023年和家人在一起的开心时刻"
                  className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors"
                />
              </div>
              
              {/* 时间范围 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  时间范围 <span className="text-red-500">*</span>
                </label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input
                    type="date"
                    name="startDate"
                    value={formData.startDate}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors"
                  />
                  <input
                    type="date"
                    name="endDate"
                    value={formData.endDate}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors"
                  />
                </div>
              </div>
              
              {/* 情绪偏好 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  情绪偏好 <span className="text-red-500">*</span>
                </label>
                <div className="flex flex-wrap gap-3">
                  {emotionOptions.map(emotion => (
                    <button
                      key={emotion.id}
                      onClick={() => setSelectedEmotion(emotion.id)}
                      className={cn(
                        "px-4 py-2 rounded-full text-sm font-medium transition-all flex items-center",
                        selectedEmotion === emotion.id
                          ? `bg-gradient-to-r ${emotion.color} text-white shadow-md`
                          : "bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600"
                      )}
                    >
                      <span className="w-3 h-3 rounded-full mr-2" style={{ 
                        background: selectedEmotion === emotion.id 
                          ? 'white' 
                          : `linear-gradient(to right, var(--tw-gradient-stops))`,
                        '--tw-gradient-from': emotion.color.split(' ')[1],
                        '--tw-gradient-to': emotion.color.split(' ')[3]
                      }}></span>
                      {emotion.name}
                    </button>
                  ))}
                </div>
              </div>
              
              {/* 风格偏好 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  风格偏好 <span className="text-red-500">*</span>
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                  {styleOptions.map(style => (
                    <button
                      key={style.id}
                      onClick={() => setSelectedStyle(style.id)}
                      className={cn(
                        "p-4 rounded-xl text-left transition-all border",
                        selectedStyle === style.id
                          ? "border-purple-500 bg-purple-50 dark:bg-purple-900/30 shadow-md"
                          : "border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-750"
                      )}
                    >
                      <h3 className="font-medium text-gray-900 dark:text-white">{style.name}</h3>
                      <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">{style.description}</p>ß
                    </button>
                  ))}
                </div>
              </div>
              
              {/* 生成按钮 */}
              <div className="pt-4 flex justify-center">
                <button
                  onClick={handleGeneratePlan}
                  disabled={isGenerating}
                  className="px-8 py-3.5 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-full font-medium shadow-lg hover:shadow-xl transition-all disabled:opacity-70 disabled:cursor-not-allowed flex items-center"
                >
                  {isGenerating ? (
                    <>
                      <i className="fa-solid fa-spinner fa-spin mr-2"></i>
                      生成中...
                    </>
                  ) : (
                    <>
                      <i className="fa-solid fa-magic mr-2"></i>
                      生成策展方案
                    </>
                  )}
                </button>
              </div>
            </div>
          </motion.div>
        )}
        
        {/* AI推荐结果区 */}
        {activeStep === 'results' && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-10"
          >
            {/* 素材预览区 */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 md:p-8">
              <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-200">AI精选素材</h2>
              
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
                {mockMaterials.map(material => (
                  <div key={material.id} className="relative group rounded-xl overflow-hidden aspect-square">
                    <img 
                      src={material.thumbnail} 
                      alt={`素材 ${material.id}`}
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                      <button className="p-2 bg-white rounded-full text-gray-900 hover:bg-gray-100">
                        <i className="fa-solid fa-eye"></i>
                      </button>
                    </div>
                    {material.type === 'recording' && (
                      <div className="absolute bottom-2 right-2 bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">
                        <i className="fa-solid fa-microphone mr-1"></i> 音频
                      </div>
                    )}
                    {material.type === 'note' && (
                      <div className="absolute bottom-2 right-2 bg-blue-500 text-white text-xs px-2 py-0.5 rounded-full">
                        <i className="fa-solid fa-file-text mr-1"></i> 笔记
                      </div>
                    )}
                  </div>
                ))}
              </div>
              
              <div className="mt-6 text-center">
                <button className="text-sm text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 font-medium flex items-center mx-auto">
                  <i className="fa-solid fa-refresh mr-1"></i> 更换部分素材
                </button>
              </div>
            </div>
            
            {/* 可视化形式推荐区 */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 md:p-8">
              <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-200">推荐可视化形式</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {visualizationOptions.map(option => (
                  <div 
                    key={option.id}
                    onClick={() => setSelectedVisualization(option.id)}
                    className={cn(
                      "rounded-xl overflow-hidden border transition-all cursor-pointer group",
                      selectedVisualization === option.id
                        ? "border-purple-500 shadow-xl"
                        : "border-gray-200 dark:border-gray-700 hover:shadow-lg"
                    )}
                  >
                    <div className="aspect-video overflow-hidden">
                      <img 
                        src={option.thumbnail} 
                        alt={option.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                    </div>
                    <div className="p-4">
                      <h3 className="font-bold text-lg mb-1 text-gray-900 dark:text-white">{option.name}</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">{option.description}</p>
                      {selectedVisualization === option.id && (
                        <div className="mt-3 w-full h-1 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"></div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            {/* 方案调整和生成按钮 */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 md:p-8">
              <div className="flex flex-col md:flex-row justify-between items-center gap-6">
                <button
                  onClick={handleBackToEdit}
                  className="px-6 py-3 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-full font-medium transition-colors flex items-center"
                >
                  <i className="fa-solid fa-arrow-left mr-2"></i>
                  返回修改
                </button>
                
                <div className="flex flex-col sm:flex-row gap-4 w-full md:w-auto">
                  <button className="px-6 py-3 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-full font-medium transition-colors flex items-center justify-center flex-1 sm:flex-none">
                    <i className="fa-solid fa-sliders mr-2"></i>
                    调整方案
                  </button>
                  
                  <button
                    onClick={handleGenerateFinal}
                    className="px-8 py-3.5 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-full font-medium shadow-lg hover:shadow-xl transition-all flex items-center justify-center flex-1 sm:flex-none"
                  >
                    <i className="fa-solid fa-star mr-2"></i>
                    生成最终作品
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </div>
      
      {/* 页脚 */}
      <Footer />
    </div>
  );
}