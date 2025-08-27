import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

// 时间轴组件
interface TimelineProps {
  data: {
    year: number;
    months: number[];
  }[];
  activeView: 'year' | 'month' | 'day';
  selectedDate: string;
  onDateSelect: (date: string) => void;
}

// 生成月份名称
const getMonthName = (month: number) => {
  const months = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];
  return months[month - 1];
};

export default function Timeline({ data, activeView, selectedDate, onDateSelect }: TimelineProps) {
  // 解析选中的日期
  const [selectedYear, selectedMonth] = selectedDate.split('-').map(Number);
  
  // 渲染年视图
  const renderYearView = () => {
    return (
      <div className="relative">
        {/* 连接线 */}
        <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-gray-300 dark:bg-gray-700 transform -translate-x-1/2"></div>
        
        <div className="space-y-12 relative z-10">
          {data.map((yearData, index) => (
            <div key={yearData.year} className="flex justify-center">
              <motion.button
                onClick={() => onDateSelect(`${yearData.year}`)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.98 }}
                className={cn(
                  "w-32 h-16 flex items-center justify-center rounded-full font-bold text-xl relative",
                  selectedYear === yearData.year
                    ? "bg-blue-600 text-white shadow-lg shadow-blue-500/20"
                    : "bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-700 shadow-sm hover:shadow-md"
                )}
              >
                {yearData.year}
                {selectedYear === yearData.year && (
                  <motion.div 
                    className="absolute -bottom-2 w-3 h-3 bg-blue-600 rounded-full"
                    animate={{ y: [0, 10, 0] }}
                    transition={{ repeat: Infinity, duration: 2 }}
                  />
                )}
              </motion.button>
            </div>
          ))}
        </div>
      </div>
    );
  };
  
  // 渲染月视图
  const renderMonthView = () => {
    // 找到当前选中年份的数据
    const currentYearData = data.find(item => item.year === selectedYear) || data[0];
    
    return (
      <div className="relative py-8">
        {/* 年份标题 */}
        <div className="text-center mb-10">
          <h3 className="text-2xl font-bold text-gray-800 dark:text-gray-200">
            {selectedYear}
          </h3>
        </div>
        
        {/* 连接线 */}
        <div className="absolute left-0 right-0 top-1/2 h-0.5 bg-gray-300 dark:bg-gray-700 transform -translate-y-1/2"></div>
        
        <div className="flex justify-between relative z-10">
          {Array.from({ length: 12 }, (_, i) => i + 1).map(month => {
            const hasMemories = currentYearData.months.includes(month);
            
            return (
              <motion.button
                key={month}
                onClick={() => onDateSelect(`${selectedYear}-${month.toString().padStart(2, '0')}`)}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                className={cn(
                  "flex flex-col items-center w-16",
                  selectedMonth === month 
                    ? "scale-110" 
                    : "opacity-70"
                )}
              >
                <div className={cn(
                  "w-10 h-10 rounded-full flex items-center justify-center font-medium mb-2",
                  selectedMonth === month 
                    ? "bg-blue-600 text-white shadow-lg shadow-blue-500/20" 
                    : hasMemories 
                      ? "bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-700"
                      : "bg-gray-100 dark:bg-gray-800 text-gray-400 dark:text-gray-500 border border-gray-200 dark:border-gray-700"
                )}>
                  {month}
                </div>
                <span className="text-xs text-gray-600 dark:text-gray-400">{getMonthName(month)}</span>
                
                {/* 有记忆的月份标记 */}
                {hasMemories && !selectedMonth === month && (
                  <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-1"></div>
                )}
              </motion.button>
            );
          })}
        </div>
      </div>
    );
  };
  
  // 渲染日视图 - 简化版实现
  const renderDayView = () => {
    // 在实际应用中，这里会根据选中的年月渲染具体日期
    // 这里简化处理，只显示一个提示
    return (
      <div className="py-12 text-center">
        <div className="inline-flex items-center px-6 py-3 bg-gray-100 dark:bg-gray-800 rounded-full text-gray-700 dark:text-gray-300">
          <i className="fa-solid fa-calendar-day mr-2"></i>
          <span className="font-medium">{selectedYear}年{selectedMonth}月</span>
          <span className="mx-2">•</span>
          <span>日视图功能即将上线</span>
        </div>
      </div>
    );
  };
  
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6 md:p-8 min-h-[200px]">
      {activeView === 'year' && renderYearView()}
      {activeView === 'month' && renderMonthView()}
      {activeView === 'day' && renderDayView()}
    </div>
  );
}