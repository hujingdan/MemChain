"""
global_constants.py - 全局常量与枚举定义

核心作用：
1. 统一定义前后端共享的业务常量（情绪、天气、标签）
2. 提供统一的成功/错误响应格式函数
3. 提供工具函数（如根据情绪分值反查标签）

修改原则：
- 所有业务常量必须在此定义，禁止在Controller/Service中硬编码
- 新增常量时需要同步更新前端 constants.js
"""

from typing import Dict, List, Optional


# ========== 情绪标签体系 ==========
# 分值范围：-100 ~ +100，共8个等级
# 每个情绪包含：分值锚点、中文标签、展示颜色、emoji图标

EMOTION_MAP: Dict[str, Dict] = {
    "ecstasy": {
        "score": 100,
        "label": "狂喜",
        "color": "#FF6B6B",
        "icon": "\U0001F929",  # 🤩
    },
    "joy": {
        "score": 75,
        "label": "开心",
        "color": "#FFD93D",
        "icon": "\U0001F600",  # 😀
    },
    "content": {
        "score": 40,
        "label": "平静",
        "color": "#6BCB77",
        "icon": "\U0001F60C",  # 😌
    },
    "neutral": {
        "score": 0,
        "label": "平淡",
        "color": "#B8B8B8",
        "icon": "\U0001F610",  # 😐
    },
    "disappointed": {
        "score": -40,
        "label": "失落",
        "color": "#9FB4CC",
        "icon": "\U0001F614",  # 😔
    },
    "sad": {
        "score": -65,
        "label": "难过",
        "color": "#5B8DB8",
        "icon": "\U0001F622",  # 😢
    },
    "angry": {
        "score": -85,
        "label": "愤怒",
        "color": "#E84545",
        "icon": "\U0001F620",  # 😠
    },
    "despair": {
        "score": -100,
        "label": "绝望",
        "color": "#4A0E0E",
        "icon": "\U0001F62D",  # 😭
    },
}

# 情绪分值 → 最近的标签（用于根据VADER分值反查情绪）
def get_emotion_by_score(score: int) -> Dict:
    """
    根据情绪分值找到最接近的情绪标签。
    
    参数:
        score: 情绪分值，范围 -100 ~ +100
    
    返回:
        {"key": "joy", "score": 75, "label": "开心", "color": "#FFD93D", "icon": "😀"}
    """
    closest_key = None
    min_diff = float("inf")
    
    for key, emotion in EMOTION_MAP.items():
        diff = abs(emotion["score"] - score)
        if diff < min_diff:
            min_diff = diff
            closest_key = key
    
    result = EMOTION_MAP[closest_key].copy()
    result["key"] = closest_key
    return result


# 获取所有情绪列表（用于前端选择器）
def get_all_emotions() -> List[Dict]:
    """返回所有情绪的完整信息列表，按分值从高到低排序"""
    return [
        {"key": k, **v} for k, v in sorted(
            EMOTION_MAP.items(), key=lambda x: x[1]["score"], reverse=True
        )
    ]


# ========== 天气类型 ==========
WEATHER_TYPES: List[Dict] = [
    {"key": "sunny",   "label": "晴朗", "icon": "\u2600"},       # ☀
    {"key": "cloudy",  "label": "多云", "icon": "\u2601"},       # ☁
    {"key": "rainy",   "label": "下雨", "icon": "\U0001F327"},  # 🌧
    {"key": "snowy",   "label": "下雪", "icon": "\u2744"},       # ❄
    {"key": "windy",   "label": "大风", "icon": "\U0001F32C"},  # 🌬
    {"key": "foggy",   "label": "雾霾", "icon": "\U0001F32B"},  # 🌫
    {"key": "thunder", "label": "雷雨", "icon": "\u26C8"},       # ⛈
]


# ========== 系统预设标签 ==========
# 用户首次使用时自动创建这些标签
SYSTEM_TAGS: List[Dict] = [
    {"name": "家庭", "color": "#E88B7C"},
    {"name": "工作", "color": "#5B8DB8"},
    {"name": "旅行", "color": "#6BCB77"},
    {"name": "健康", "color": "#FFD93D"},
    {"name": "回忆", "color": "#C9B1FF"},
    {"name": "学习", "color": "#FF9F45"},
    {"name": "美食", "color": "#FF6B6B"},
    {"name": "友情", "color": "#95D1CC"},
]


# ========== 文件相关常量 ==========
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB（字节）

# MIME类型前缀 → 存储子目录映射
ALLOWED_MIME_TYPES = {
    "image/": "images",
    "audio/": "audio",
    "text/": "text",
    "application/pdf": "documents",
}

# 所有允许的MIME类型前缀（扁平化列表，用于快速检查）
ALL_ALLOWED_TYPE_PREFIXES = list(ALLOWED_MIME_TYPES.keys())

# 文件扩展名 → MIME类型映射
EXTENSION_MIME_MAP = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".png": "image/png", ".gif": "image/gif",
    ".bmp": "image/bmp", ".webp": "image/webp",
    ".mp3": "audio/mpeg", ".wav": "audio/wav",
    ".txt": "text/plain", ".pdf": "application/pdf",
}


# ========== 统一响应格式 ==========
def success_response(data=None, message: str = "操作成功") -> Dict:
    """
    统一成功响应格式。
    所有接口返回成功时都必须使用此函数包装。
    """
    return {
        "success": True,
        "message": message,
        "data": data,
    }

def error_response(message: str = "操作失败", detail: str = None, code: int = 400) -> Dict:
    """
    统一错误响应格式。
    所有接口返回错误时都必须使用此函数包装。
    """
    return {
        "success": False,
        "message": message,
        "detail": detail,
        "code": code,
    }


# ========== 分页默认值 ==========
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


# ========== JWT配置（Phase 2使用）==========
JWT_SECRET_KEY = "memchain-dev-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_DAYS = 7