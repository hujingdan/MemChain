"""
MemChain AI功能测试脚本

快速测试Level 1的AI分析功能是否正常工作

使用方法：
    python test_ai_analysis.py --photo path/to/photo.jpg
    python test_ai_analysis.py --text path/to/note.txt

注意：
    1. 确保后端服务已启动（python -m uvicorn app:app --reload）
    2. 确保已在.env中配置了VOLCENGINE_API_KEY
"""

import os
import sys
import time
import argparse
from pathlib import Path
from typing import Optional

import requests

# ==================== 配置 ====================

API_BASE = "http://localhost:8000"
# 也可以通过环境变量覆盖
# API_BASE = os.getenv("MEMCHAIN_API_BASE", "http://localhost:8000")

# ==================== 工具函数 ====================

def print_section(title: str):
    """打印分节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def print_success(message: str):
    """打印成功消息"""
    print(f"✅ {message}")


def print_error(message: str):
    """打印错误消息"""
    print(f"❌ {message}")


def print_info(message: str):
    """打印信息消息"""
    print(f"ℹ️  {message}")


def print_warning(message: str):
    """打印警告消息"""
    print(f"⚠️  {message}")


def check_backend() -> bool:
    """检查后端是否运行"""
    try:
        response = requests.get(f"{API_BASE}/", timeout=5)
        return True
    except Exception as e:
        print_error(f"无法连接到后端服务 ({API_BASE})")
        print_info("请确保后端已启动：python -m uvicorn app:app --reload --port 8000")
        return False


# ==================== API调用 ====================

def upload_file(file_path: str) -> Optional[str]:
    """
    上传文件到MemChain

    Args:
        file_path: 文件路径

    Returns:
        Material ID，失败返回None
    """
    print_section("步骤 1: 上传文件")

    if not os.path.exists(file_path):
        print_error(f"文件不存在: {file_path}")
        return None

    file_name = os.path.basename(file_path)
    print_info(f"上传文件: {file_name}")

    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_name, f, 'application/octet-stream')}
            response = requests.post(
                f"{API_BASE}/upload/direct",
                files=files,
                timeout=60
            )

        if response.status_code == 200:
            data = response.json()
            material_id = data.get('id')
            print_success(f"上传成功！")
            print_info(f"Material ID: {material_id}")
            print_info(f"文件大小: {data.get('size', 0)} bytes")
            print_info(f"文件类型: {data.get('type', 'unknown')}")
            return material_id
        else:
            print_error(f"上传失败 (状态码: {response.status_code})")
            print_error(response.text)
            return None

    except Exception as e:
        print_error(f"上传过程出错: {e}")
        return None


def analyze_material(material_id: str, force_refresh: bool = False) -> Optional[dict]:
    """
    分析Material（情感+标签+描述）

    Args:
        material_id: Material ID
        force_refresh: 是否强制重新分析

    Returns:
        分析结果字典
    """
    print_section("步骤 2: AI分析")

    print_info(f"开始分析 Material: {material_id}")
    print_warning("这可能需要10-30秒，请耐心等待...")
    print()

    start_time = time.time()

    try:
        payload = {
            "material_id": material_id,
            "force_refresh": force_refresh
        }

        response = requests.post(
            f"{API_BASE}/api/ai/analyze",
            json=payload,
            timeout=120  # 2分钟超时
        )

        elapsed = time.time() - start_time

        if response.status_code == 200:
            print_success(f"分析完成！耗时: {elapsed:.1f}秒")
            return response.json()
        else:
            print_error(f"分析失败 (状态码: {response.status_code})")
            print_error(response.text)
            return None

    except Exception as e:
        print_error(f"分析过程出错: {e}")
        return None


def display_analysis_result(result: dict):
    """
    美化显示分析结果

    Args:
        result: 分析结果字典
    """
    print_section("步骤 3: 查看结果")

    # 情感分析
    emotion = result.get('emotion', {})
    print("💭 情感分析")
    print(f"   主要情感: {emotion.get('primary', 'N/A')}")
    print(f"   情感强度: {emotion.get('confidence', 0):.2%}")
    print(f"   情感描述: {emotion.get('description', 'N/A')}")
    print()

    # 标签
    tags = result.get('tags', [])
    categories = result.get('tag_categories', {})
    print("🏷️  标签生成")
    if tags:
        print(f"   所有标签: {', '.join(tags[:10])}")
        if len(tags) > 10:
            print(f"   ... 还有 {len(tags) - 10} 个标签")

        # 按类别显示
        for category, items in categories.items():
            if items:
                print(f"   {category}: {', '.join(items)}")
    else:
        print("   未生成标签")
    print()

    # 内容描述
    description = result.get('description', {})
    print("📝 内容描述")
    print(f"   摘要: {description.get('summary', 'N/A')}")
    print(f"   详细: {description.get('detail', 'N/A')[:100]}...")
    print()

    # 关键元素
    key_elements = description.get('key_elements', [])
    if key_elements:
        print(f"🔑 关键元素: {', '.join(key_elements[:8])}")


def get_cached_analysis(material_id: str) -> Optional[dict]:
    """
    获取缓存的分析结果

    Args:
        material_id: Material ID

    Returns:
        分析结果字典
    """
    print_section("获取缓存结果")

    try:
        response = requests.get(
            f"{API_BASE}/api/ai/material/{material_id}",
            timeout=10
        )

        if response.status_code == 200:
            print_success("找到缓存的分析结果")
            return response.json()
        elif response.status_code == 404:
            print_warning("该Material尚未进行分析")
            return None
        else:
            print_error(f"获取失败 (状态码: {response.status_code})")
            return None

    except Exception as e:
        print_error(f"获取过程出错: {e}")
        return None


# ==================== 主程序 ====================

def main():
    parser = argparse.ArgumentParser(
        description="MemChain AI功能测试脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python test_ai_analysis.py --photo photo.jpg
  python test_ai_analysis.py --text note.txt
  python test_ai_analysis.py --photo photo.jpg --force
        """
    )

    parser.add_argument(
        '--photo',
        type=str,
        help='照片文件路径（支持jpg, png等）'
    )

    parser.add_argument(
        '--text',
        type=str,
        help='文本文件路径（支持txt, md等）'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='强制重新分析（忽略缓存）'
    )

    parser.add_argument(
        '--material-id',
        type=str,
        help='直接使用已存在的Material ID（跳过上传）'
    )

    args = parser.parse_args()

    # 打印欢迎信息
    print("\n" + "="*60)
    print("  MemChain AI 功能测试")
    print("="*60 + "\n")

    # 检查后端
    if not check_backend():
        sys.exit(1)

    # 确定要分析的文件或Material ID
    material_id = None
    file_path = None

    if args.material_id:
        material_id = args.material_id
        print_info(f"使用现有Material ID: {material_id}")
        print()
    elif args.photo:
        file_path = args.photo
    elif args.text:
        file_path = args.text
    else:
        print_error("请指定 --photo 或 --text 参数")
        parser.print_help()
        sys.exit(1)

    # 上传文件（如果需要）
    if file_path:
        material_id = upload_file(file_path)
        if not material_id:
            sys.exit(1)

    # 检查是否有缓存
    if not args.force:
        cached = get_cached_analysis(material_id)
        if cached:
            display_analysis_result(cached)
            print()
            print_info("💡 使用 --force 参数可以强制重新分析")
            print_success("测试完成！")
            sys.exit(0)

    # 执行AI分析
    result = analyze_material(material_id, force_refresh=args.force)

    if result:
        display_analysis_result(result)
        print()
        print_success("✨ 测试成功！所有功能正常工作")
        print()
        print_info("💡 提示：")
        print("   - 查看API文档: http://localhost:8000/docs")
        print("   - 查看Material详情:访问 {}/api/ai/material/{}".format(
            API_BASE, material_id
        ))
        sys.exit(0)
    else:
        print_error("测试失败！请检查：")
        print("   1. 后端是否正常运行")
        print("   2. .env文件中是否配置了VOLCENGINE_API_KEY")
        print("   3. 网络连接是否正常")
        print("   4. API密钥是否有足够额度")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\n\n测试被用户中断")
        sys.exit(0)
