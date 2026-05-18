"""
timeline_controller.py - 时间轴与仪表盘数据接口
为记忆长廊首页提供情绪折线图数据、统计数字、最近记忆列表。
"""
import uuid
from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Query, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Material, Emotion
from ...global_constants import success_response, error_response, EMOTION_MAP

router = APIRouter()


@router.get("/emotions")
async def get_emotion_timeline(
    days: int = Query(default=30, ge=7, le=365, description="查询天数范围，7-365"),
    db: Session = Depends(get_db)
):
    """
    获取情绪时间轴数据，用于ECharts折线图。
    返回最近N天内的所有情绪记录，按日期排序。
    
    返回格式：
    {
      "dates": ["05-01", "05-02", ...],
      "scores": [80, -20, 40, ...],
      "emotions": [{"label": "开心", "color": "#FFD93D", "icon": "😀"}, ...]
    }
    """
    start_date = datetime.now() - timedelta(days=days)
    
    # 查询时间范围内的情绪记录
    emotions = db.query(Emotion).filter(
        Emotion.recorded_at >= start_date
    ).order_by(Emotion.recorded_at.asc()).all()
    
    # 按天聚合：同一天有多条记录时取平均分
    daily_emotions = {}
    for e in emotions:
        date_key = e.recorded_at.strftime("%m-%d")
        if date_key not in daily_emotions:
            daily_emotions[date_key] = []
        daily_emotions[date_key].append(e)
    
    dates = []
    scores = []
    emotion_details = []
    
    for date_key in sorted(daily_emotions.keys()):
        day_records = daily_emotions[date_key]
        avg_score = sum(r.score for r in day_records) / len(day_records)
        
        # 取平均分值最近的情绪标签
        closest = min(EMOTION_MAP.items(), key=lambda x: abs(x[1]["score"] - avg_score))
        
        dates.append(date_key)
        scores.append(round(avg_score))
        emotion_details.append({
            "label": closest[1]["label"],
            "key": closest[0],
            "color": closest[1]["color"],
            "icon": closest[1]["icon"],
            "count": len(day_records),
        })
    
    return success_response(data={
        "dates": dates,
        "scores": scores,
        "emotions": emotion_details,
    })


@router.get("/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    获取仪表盘统计数字。
    返回：总素材数、总情绪记录数、本月新增素材数、平均情绪分
    """
    # 总素材数
    total_materials = db.query(func.count(Material.id)).scalar() or 0
    
    # 总情绪记录数
    total_emotions = db.query(func.count(Emotion.id)).scalar() or 0
    
    # 本月新增素材数
    this_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0)
    this_month_materials = db.query(func.count(Material.id)).filter(
        Material.created_at >= this_month_start
    ).scalar() or 0
    
    # 平均情绪分
    avg_emotion = db.query(func.avg(Emotion.score)).scalar()
    avg_emotion = round(avg_emotion) if avg_emotion else 0
    
    # 按类型统计素材数量
    type_stats = {}
    for type_name in ["images", "audio", "text", "documents", "others"]:
        count = db.query(func.count(Material.id)).filter(
            Material.type == type_name
        ).scalar() or 0
        type_stats[type_name] = count
    
    return success_response(data={
        "total_materials": total_materials,
        "total_emotions": total_emotions,
        "this_month_materials": this_month_materials,
        "avg_emotion": avg_emotion,
        "type_stats": type_stats,
    })


@router.get("/entries/recent")
async def get_recent_entries(
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    获取最近的记忆条目（模拟数据，Phase 3替换为真实entries表查询）。
    当前返回最近上传的文件作为"记忆卡片"数据源。
    """
    materials = db.query(Material).filter(
        Material.is_deleted == False
    ).order_by(Material.created_at.desc()).limit(limit).all()
    
    items = []
    for m in materials:
        items.append({
            "id": m.id,
            "title": m.name or "未命名",
            "type": m.type,
            "mime_type": m.mime_type,
            "size": m.size,
            "created_at": m.created_at.isoformat() if m.created_at else None,
            "properties": m.properties or {},
            "is_archived": m.is_archived,
        })
    
    return success_response(data={
        "items": items,
        "total": len(items),
    })


@router.post("/emotions/seed")
async def seed_emotion_data(db: Session = Depends(get_db)):
    """
    【开发辅助接口】生成30天的模拟情绪数据，用于测试折线图。
    仅开发环境使用，生产环境应删除。
    """
    import random
    
    emotion_keys = list(EMOTION_MAP.keys())
    
    for i in range(30):
        date = datetime.now() - timedelta(days=29-i)
        key = random.choice(emotion_keys)
        emotion_info = EMOTION_MAP[key]
        
        # 在锚点分值附近随机波动 ±15
        score = emotion_info["score"] + random.randint(-15, 15)
        score = max(-100, min(100, score))  # 限制在-100~+100
        
        e = Emotion(
            id=str(uuid.uuid4()),
            user_id="demo_user",
            score=score,
            label=key,
            recorded_at=date,
        )
        db.add(e)
    
    db.commit()
    return success_response(message="已生成30天模拟情绪数据")