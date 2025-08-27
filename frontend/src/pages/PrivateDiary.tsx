import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { toast } from 'sonner';

// 模拟表情数据 (简化版) - 实际项目中可以使用更完整的数据
const emojis = [
  { category: '表情', icons: ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇'] },
  { category: '人物', icons: ['👋', '🤚', '🖐️', '✋', '🖖', '👌', '👍', '👎', '👏', '🙌'] },
  { category: '自然', icons: ['☀️', '🌤️', '⛅', '🌥️', '☁️', '🌧️', '⛈️', '🌩️', '🌨️', '❄️'] },
  { category: '食物', icons: ['🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍒'] },
];

// 模拟记忆库素材数据
const memoryMaterials = [
  {
    id: 1,
    type: 'photo',
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=family%20dinner%20photo%20warm%20lighting&sign=c904e2981f3d492923391bf2146b0612',
    date: '2023-10-01',
    title: '家庭聚餐'
  },
  { 
    id: 2, 
    type: 'photo', 
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=birthday%20celebration%20candle%20cake&sign=3da0cde270322cbfa5c110f56d36f452', 
    date: '2023-10-02',
    title: '生日派对' 
  },
  { 
    id: 3, 
    type: 'recording', 
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=audio%20waveform%20visualization%20blue&sign=84181560d83f378bb1b613b82073ba4d', 
    date: '2023-10-03',
    title: '奶奶的故事' 
  },
  { 
    id: 4, 
    type: 'photo', 
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=sunset%20over%20mountain%20landscape&sign=8338e0ea0df8a87f8569f87f00eb4c26', 
    date: '2023-10-05',
    title: '山顶日落' 
  },
  { 
    id: 5, 
    type: 'note', 
    thumbnail: 'https://space.coze.cn/api/coze_space/gen_image?image_size=square&prompt=handwritten%20note%20paper%20texture&sign=c3dee662709b7a0c3418a1ed84af4e70', 
    date: '2023-10-07',
    title: '旅行笔记' 
  },
];

// 模拟AI情感分析结果
const aiAnalysisResult = {
  emotion: '平静',
  score: 0.85,
  keywords: ['宁静', '回忆', '感恩', '思考'],
  interpretation: '您的日记表达了一种平静而感恩的情绪，充满了对美好回忆的珍视和对生活的思考。',
  relatedMemories: [
    { id: 1, title: '去年今日的日记', similarity: 0.92 },
    { id: 4, title: '山顶日落的照片', similarity: 0.78 },
    { id: 5, title: '旅行笔记中的思考', similarity: 0.65 },
  ]
};

export default function PrivateDiary() {
  // 状态管理
  const [diaryContent, setDiaryContent] = useState('');
  const [isPasswordProtected, setIsPasswordProtected] = useState(false);
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [selectedEmojiCategory, setSelectedEmojiCategory] = useState('表情');
  const [selectedMaterials, setSelectedMaterials] = useState<number[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [aiAnalysis, setAiAnalysis] = useState<any>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [isEditorFocused, setIsEditorFocused] = useState(false);

  // 处理表情插入
  const handleEmojiSelect = (emoji: string) => {
    setDiaryContent(prev => prev + emoji);
    setShowEmojiPicker(false);
  };

  // 处理素材选择
  const toggleMaterialSelection = (materialId: number) => {
    setSelectedMaterials(prev => 
      prev.includes(materialId)
        ? prev.filter(id => id !== materialId)
        : [...prev, materialId]
    );
  };

  // 处理密码保护切换
  const handlePasswordProtectionToggle = () => {
    if (!isPasswordProtected && (!password || password !== confirmPassword)) {
      toast.error('密码不一致或未设置，请检查');
      return;
    }
    
    setIsPasswordProtected(!isPasswordProtected);
    
    if (isPasswordProtected) {
      toast.success('已取消密码保护');
    } else {
      toast.success('已启用密码保护');
    }
  };

  // 执行AI分析
  const runAiAnalysis = () => {
    if (!diaryContent.trim()) {
      toast.error('请先输入日记内容');
      return;
    }
    
    setIsAnalyzing(true);
    
    // 模拟AI分析过程
    setTimeout(() => {
      setAiAnalysis(aiAnalysisResult);
      setIsAnalyzing(false);
      toast.success('AI情感分析已完成');
    }, 1500);
  };

  // 保存日记
  const saveDiary = () => {
    if (!diaryContent.trim()) {
      toast.error('日记内容不能为空');
      return;
    }
    
    setIsSaving(true);
    
    // 模拟保存过程
    setTimeout(() => {
      setIsSaving(false);
      toast.success('日记保存成功');
      
      // 清空表单
      setDiaryContent('');
      setSelectedMaterials([]);
      setAiAnalysis(null);
      setPassword('');
      setConfirmPassword('');
    }, 1200);
  };

  // 获取选中的素材
  const getSelectedMaterials = () => {
    return memoryMaterials.filter(material => 
      selectedMaterials.includes(material.id)
    );
  };

  // 渲染情感分析结果
  const renderEmotionAnalysis = () => {
    if (!aiAnalysis) return null;
    
    // 根据情绪类型获取对应的颜色
    const getEmotionColor = () => {
      switch(aiAnalysis.emotion) {
        case '开心': return 'text-yellow-500 bg-yellow-50 dark:bg-yellow-900/20';
        case '悲伤': return 'text-blue-500 bg-blue-50 dark:bg-blue-900/20';
        case '愤怒': return 'text-red-500 bg-red-50 dark:bg-red-900/20';
        case '平静': return 'text-green-500 bg-green-50 dark:bg-green-900/20';
        case '惊讶': return 'text-purple-500 bg-purple-50 dark:bg-purple-900/20';
        default: return 'text-gray-500 bg-gray-50 dark:bg-gray-800';
      }
    };
    
    return (
      <div className="space-y-4">
        <div className={`p-4 rounded-xl ${getEmotionColor()}`}>
          <div className="flex items-center justify-between">
            <h4 className="font-medium flex items-center">
              <span className="mr-2">{aiAnalysis.emotion}</span>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                (情感强度: {(aiAnalysis.score * 100).toFixed(0)}%)
              </span>
            </h4>
            <div className="w-20 bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
              <div 
                className="bg-current h-2.5 rounded-full" 
                style={{ width: `${aiAnalysis.score * 100}%` }}
              ></div>
            </div>
          </div>
        </div>
        
        <div>
          <h4 className="font-medium mb-2 text-gray-800 dark:text-gray-200">关键词</h4>
          <div className="flex flex-wrap gap-2">
            {aiAnalysis.keywords.map((keyword: string, index: number) => (
              <span 
                key={index} 
                className="px-3 py-1 bg-gray-100 dark:bg-gray-700 rounded-full text-sm text-gray-700 dark:text-gray-300"
              >
                {keyword}
              </span>
            ))}
          </div>
        </div>
        
        <div>
          <h4 className="font-medium mb-2 text-gray-800 dark:text-gray-200">情感解读</h4>
          <p className="text-sm text-gray-600 dark:text-gray-400">{aiAnalysis.interpretation}</p>
        </div>
        
        <div>
          <h4 className="font-medium mb-2 text-gray-800 dark:text-gray-200">关联回忆推荐</h4>
          <div className="space-y-2">
            {aiAnalysis.relatedMemories.map((memory: any) => (
              <div 
                key={memory.id}
                className="p-3 bg-gray-50 dark:bg-gray-850 rounded-lg text-sm flex justify-between items-center"
              >
                <span>{memory.title}</span>
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  相似度: {(memory.similarity * 100).toFixed(0)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 text-gray-900 dark:text-gray-100">
      {/* 导航栏 */}
      <Navbar />
      
      <div className="container mx-auto px-4 py-8">
        {/* 页面标题 */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-rose-500 to-pink-600 dark:from-rose-400 dark:to-pink-500 mb-2">
            私密日记助手
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            记录内心世界，安全保存珍贵思绪
          </p>
        </div>
        
        {/* 主内容区 - 响应式布局 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* 左侧：日记编辑区 */}
          <div className="lg:col-span-2 space-y-8">
            {/* 日记编辑器卡片 */}
            <motion.div 
              className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden transition-all duration-300"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
            >
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-bold text-gray-800 dark:text-gray-200 flex items-center">
                    <i className="fa-solid fa-book-open text-rose-500 mr-3"></i>
                    日记编辑区
                  </h2>
                  <div className="flex items-center space-x-3">
                    <label className="flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={isPasswordProtected}
                        onChange={handlePasswordProtectionToggle}
                        className="sr-only peer"
                      />
                      <div className="relative w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-rose-500"></div>
                      <span className="ml-2 text-sm font-medium text-gray-700 dark:text-gray-300">密码保护</span>
                    </label>
                  </div>
                </div>
                
                {/* 密码保护设置 (仅在启用时显示) */}
                {isPasswordProtected && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 p-3 bg-gray-50 dark:bg-gray-850 rounded-xl">
                    <div>
                      <label className="block text-xs text-gray-600 dark:text-gray-400 mb-1">设置密码</label>
                      <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-sm"
                        placeholder="请设置密码"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-600 dark:text-gray-400 mb-1">确认密码</label>
                      <input
                        type="password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        className="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-sm"
                        placeholder="请确认密码"
                      />
                    </div>
                  </div>
                )}
              </div>
              
              {/* 编辑器区域 */}
              <div className={cn(
                "p-6 transition-all",
                isEditorFocused ? "border-t-2 border-rose-200 dark:border-rose-900/50" : "border-t border-gray-200 dark:border-gray-700"
              )}>
                <div className="relative">
                  <textarea
                    value={diaryContent}
                    onChange={(e) => setDiaryContent(e.target.value)}
                    onFocus={() => setIsEditorFocused(true)}
                    onBlur={() => setIsEditorFocused(false)}
                    placeholder="开始记录您的想法和感受..."
                    className="w-full min-h-[300px] p-4 bg-gray-50 dark:bg-gray-850 rounded-xl border border-gray-200 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-rose-500 resize-none text-gray-800 dark:text-gray-200 transition-all"
                  />
                  
                  {/* 字数统计 */}
                  <div className="absolute bottom-3 right-3 text-xs text-gray-500 dark:text-gray-400">
                    {diaryContent.length} 字
                  </div>
                </div>
                
                {/* 编辑器工具栏 */}
                <div className="mt-4 flex flex-wrap items-center justify-between gap-4">
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => setShowEmojiPicker(!showEmojiPicker)}
                      className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                      aria-label="插入表情"
                    >
                      <i className="fa-solid fa-face-smile"></i>
                    </button>
                    
                    {/* 表情选择器 */}
                    {showEmojiPicker && (
                      <div className="absolute z-20 mt-2 w-64 bg-white dark:bg-gray-800 rounded-xl shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
                        <div className="p-2 border-b border-gray-200 dark:border-gray-700">
                          <div className="flex space-x-1 overflow-x-auto pb-1 scrollbar-hide">
                            {emojis.map(category => (
                              <button
                                key={category.category}
                                onClick={() => setSelectedEmojiCategory(category.category)}
                                className={cn(
                                  "px-3 py-1 text-xs rounded-full whitespace-nowrap",
                                  selectedEmojiCategory === category.category
                                    ? "bg-rose-500 text-white"
                                    : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                                )}
                              >
                                {category.category}
                              </button>
                            ))}
                          </div>
                        </div>
                        <div className="p-3 grid grid-cols-5 gap-2">
                          {emojis.find(c => c.category === selectedEmojiCategory)?.icons.map((emoji, index) => (
                            <button
                              key={index}
                              onClick={() => handleEmojiSelect(emoji)}
                              className="text-xl p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                            >
                              {emoji}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    <button className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors" aria-label="加粗">
                      <i className="fa-solid fa-bold"></i>
                    </button>
                    <button className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors" aria-label="斜体">
                      <i className="fa-solid fa-italic"></i>
                    </button>
                    <button className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors" aria-label="下划线">
                      <i className="fa-solid fa-underline"></i>
                    </button>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <button 
                      onClick={() => {
                        setIsAnalyzing(true);
                        setTimeout(() => {
                          setIsAnalyzing(false);
                          setAiAnalysis(aiAnalysisResult);
                          toast.success('AI情感分析已完成');
                        }, 1500);
                      }}
                      disabled={!diaryContent.trim() || isAnalyzing}
                      className="px-4 py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg text-sm font-medium transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isAnalyzing ? (
                        <>
                          <i className="fa-solid fa-spinner fa-spin mr-2"></i>
                          分析中...
                        </>
                      ) : (
                        <>
                          <i className="fa-solid fa-lightbulb mr-2"></i>
                          AI分析
                        </>
                      )}
                    </button>
                    
                    <button 
                      onClick={saveDiary}
                      disabled={!diaryContent.trim() || isSaving}
                      className="px-4 py-2 bg-rose-500 hover:bg-rose-600 text-white rounded-lg text-sm font-medium transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isSaving ? ( 
                        <>
                          <i className="fa-solid fa-spinner fa-spin mr-2"></i>
                          保存中...
                        </>
                      ) : (
                        <>
                          <i className="fa-solid fa-save mr-2"></i>
                          保存日记
                        </>
                      )}
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
            
            {/* AI分析区 */}
            <motion.div 
              className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <h2 className="text-xl font-bold mb-6 text-gray-800 dark:text-gray-200 flex items-center">
                <i className="fa-solid fa-robot text-rose-500 mr-3"></i>
                AI分析区
              </h2>
              
              {isAnalyzing ? (
                <div className="flex flex-col items-center justify-center py-12">
                  <div className="w-16 h-16 border-4 border-t-rose-500 border-gray-200 dark:border-gray-700 rounded-full animate-spin mb-4"></div>
                  <p className="text-gray-600 dark:text-gray-400">正在进行情感分析，请稍候...</p>
                  <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">分析过程在本地进行，保护您的隐私安全</p>
                </div>
              ) : aiAnalysis ? (
                renderEmotionAnalysis()
              ) : (
                <div className="text-center py-12 bg-gray-50 dark:bg-gray-850 rounded-xl">
                  <i className="fa-solid fa-lightbulb text-3xl text-gray-400 mb-4"></i>
                  <h3 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-2">尚未进行情感分析</h3>
                  <p className="text-gray-500 dark:text-gray-400 mb-6 max-w-md mx-auto">
                    完成日记编辑后，点击"AI分析"按钮，我们将对您的日记内容进行情感解读并推荐相关回忆
                  </p>
                  <button 
                    onClick={() => {
                      setIsAnalyzing(true);
                      setTimeout(() => {
                        setIsAnalyzing(false);
                        setAiAnalysis(aiAnalysisResult);
                        toast.success('AI情感分析已完成');
                      }, 1500);
                    }}
                    disabled={!diaryContent.trim()}
                    className="px-5 py-2.5 bg-rose-500 hover:bg-rose-600 text-white rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <i className="fa-solid fa-magic mr-2"></i>
                    开始AI分析
                  </button>
                </div>
              )}
            </motion.div>
          </div>
          
          {/* 右侧：关联素材区 */}
          <div className="lg:col-span-1">
            <motion.div 
              className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 sticky top-24"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <h2 className="text-xl font-bold mb-6 text-gray-800 dark:text-gray-200 flex items-center">
                <i className="fa-solid fa-paperclip text-rose-500 mr-3"></i>
                关联素材区
              </h2>
              
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                从记忆库中选择素材添加到当前日记
              </p>
              
              <div className="space-y-3 max-h-[400px] overflow-y-auto pr-1">
                {memoryMaterials.map(material => (
                  <div 
                    key={material.id}
                    onClick={() => toggleMaterialSelection(material.id)}
                    className={cn(
                      "flex items-center p-3 rounded-xl border cursor-pointer transition-all",
                      selectedMaterials.includes(material.id)
                        ? "border-rose-500 bg-rose-50 dark:bg-rose-900/20"
                        : "border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-750"
                    )}
                  >
                    <div className="w-16 h-16 rounded-lg overflow-hidden flex-shrink-0">
                      <img 
                        src={material.thumbnail} 
                        alt={material.title}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="ml-3 flex-grow min-w-0">
                      <h3 className="text-sm font-medium text-gray-900 dark:text-white truncate">{material.title}</h3>
                      <p className="text-xs text-gray-500 dark:text-gray-400">{material.date}</p>
                    </div>
                    <div className={`ml-2 w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 ${
                      selectedMaterials.includes(material.id)
                        ? 'bg-rose-500 text-white'
                        : 'bg-gray-200 dark:bg-gray-700'
                    }`}>
                      {selectedMaterials.includes(material.id) && (
                        <i className="fa-solid fa-check text-xs"></i>
                      )}
                    </div>
                  </div>
                ))}
              </div>
              
              {selectedMaterials.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-sm text-gray-700 dark:text-gray-300">
                      已选择 {selectedMaterials.length} 个素材
                    </span>
                    <button 
                      onClick={() => setSelectedMaterials([])}
                      className="text-xs text-rose-500 hover:text-rose-600 dark:text-rose-400 dark:hover:text-rose-300"
                    >
                      清除全部
                    </button>
                  </div>
                  <button className="w-full py-2 bg-rose-500 hover:bg-rose-600 text-white rounded-lg text-sm font-medium transition-colors">
                    <i className="fa-solid fa-link mr-1"></i> 关联选中素材
                  </button>
                </div>
              )}
            
              {/* 本地处理说明 */}
              <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
                <div className="flex items-start">
                  <i className="fa-solid fa-shield text-rose-500 mt-0.5 mr-2"></i>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    所有AI分析和密码保护均在本地处理，您的日记内容不会上传到云端，确保隐私安全。
                  </p>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
      
      {/* 页脚 */}
      <Footer />
    </div>
  );
}