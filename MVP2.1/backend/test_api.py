"""
测试后端API功能
"""
import requests
import json
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """测试健康检查"""
    print("\n" + "="*70)
    print("【1】测试健康检查 API")
    print("="*70)

    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_upload_init():
    """测试文件上传初始化"""
    print("\n" + "="*70)
    print("【2】测试文件上传初始化")
    print("="*70)

    # 创建一个测试文件
    test_file = Path("test_image.jpg")
    if not test_file.exists():
        print("⚠️  测试文件不存在，跳过上传测试")
        print("提示：请在backend目录下放一个测试文件 test_image.jpg")
        return None

    try:
        with open(test_file, 'rb') as f:
            files = {'file': (test_file.name, f, 'image/jpeg')}
            data = {'chunk_index': '0', 'total_chunks': '1'}

            response = requests.post(f"{BASE_URL}/upload/init", files=files, data=data)
            print(f"状态码: {response.status_code}")
            print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            return response.status_code == 200
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_ai_analyze():
    """测试AI分析API（需要材料ID）"""
    print("\n" + "="*70)
    print("【3】测试AI分析API")
    print("="*70)

    # 这个需要先有材料才能测试
    print("⚠️  需要先上传文件获取材料ID")
    print("示例命令:")
    print(f"  curl -X POST {BASE_URL}/api/ai/analyze/emotion \\")
    print(f"    -H 'Content-Type: application/json' \\")
    print(f"    -d '{{\"material_id\": 1}}'")

def list_routes():
    """列出所有可用的路由"""
    print("\n" + "="*70)
    print("【4】可用的API路由")
    print("="*70)

    routes = [
        ("GET", "/health", "健康检查"),
        ("POST", "/upload/init", "初始化文件上传"),
        ("POST", "/upload/chunk", "上传文件分块"),
        ("POST", "/upload/complete", "完成文件上传"),
        ("POST", "/upload/cancel", "取消文件上传"),
        ("GET", "/upload/status/{upload_id}", "获取上传状态"),
        ("POST", "/api/ai/analyze", "完整AI分析（情感+标签+描述）"),
        ("POST", "/api/ai/analyze/emotion", "情感分析"),
        ("POST", "/api/ai/analyze/tags", "标签生成"),
        ("POST", "/api/ai/analyze/description", "内容描述"),
        ("GET", "/api/ai/material/{id}", "获取材料AI分析结果"),
        ("POST", "/api/relationships/embedding/generate", "生成嵌入向量"),
        ("POST", "/api/relationships/similarity/calculate", "计算相似度"),
        ("POST", "/api/relationships/build", "构建材料关系"),
        ("GET", "/api/relationships/{id}", "获取材料关系"),
    ]

    for method, route, description in routes:
        print(f"  {method:6} {route:50} - {description}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  MemChain后端API测试")
    print("="*70)
    print(f"服务器地址: {BASE_URL}")
    print("请确保后端服务器正在运行！")
    print()

    # 运行测试
    test_health_check()
    test_upload_init()
    test_ai_analyze()
    list_routes()

    print("\n" + "="*70)
    print("测试完成")
    print("="*70)
