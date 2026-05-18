# MemChain AI功能测试指南

本指南帮助你快速测试MemChain的AI分析功能是否正常工作。

---

## 📋 前置条件

1. **后端服务已启动**
   ```bash
   cd MVP/backend
   python -m uvicorn app:app --reload --port 8000
   ```

2. **环境变量已配置**
   ```bash
   cd MVP/backend
   # 确保.env文件存在且包含有效的API密钥
   cat .env | grep VOLCENGINE_API_KEY
   ```

3. **数据库已初始化**
   ```bash
   cd MVP/backend
   alembic upgrade head
   ```

---

## 🧪 测试方法

### 方法1：使用测试脚本（推荐）

这是最简单的测试方法。

#### 测试图片分析

```bash
cd MVP/backend

# 使用你自己的照片
python test_ai_analysis.py --photo /path/to/your/photo.jpg

# 或者使用示例图片（如果有的话）
python test_ai_analysis.py --photo ../test-data/sample-photo.jpg
```

#### 测试文本分析

```bash
# 创建一个测试文本文件
echo "今天是一个美好的日子，阳光明媚，心情格外舒畅。" > test-note.txt

# 运行测试
python test_ai_analysis.py --text test-note.txt
```

#### 强制重新分析（忽略缓存）

```bash
python test_ai_analysis.py --photo photo.jpg --force
```

#### 使用已存在的Material ID

```bash
# 如果之前上传过文件，可以直接用ID测试
python test_ai_analysis.py --material-id abc-123-def-456
```

---

### 方法2：使用API文档（Swagger UI）

1. 打开浏览器访问：http://localhost:8000/docs
2. 找到 `POST /upload/direct` 端点
3. 点击 "Try it out"
4. 上传一张图片
5. 复制返回的 `id` 字段
6. 找到 `POST /api/ai/analyze` 端点
7. 粘贴 `id` 到 `material_id` 字段
8. 点击 "Execute"
9. 等待结果

---

### 方法3：使用cURL命令

```bash
# 1. 上传图片
curl -X POST "http://localhost:8000/upload/direct" \
  -F "file=@/path/to/photo.jpg"

# 假设返回：{"id": "abc-123...", ...}

# 2. 分析图片
curl -X POST "http://localhost:8000/api/ai/analyze" \
  -H "Content-Type: application/json" \
  -d '{"material_id": "abc-123...", "force_refresh": false}'
```

---

### 方法4：使用Python代码

创建 `my_test.py`:

```python
import requests

API_BASE = "http://localhost:8000"

# 1. 上传
with open("photo.jpg", "rb") as f:
    upload_resp = requests.post(
        f"{API_BASE}/upload/direct",
        files={"file": f}
    )
    material_id = upload_resp.json()["id"]
    print(f"上传成功: {material_id}")

# 2. 分析
analyze_resp = requests.post(
    f"{API_BASE}/api/ai/analyze",
    json={"material_id": material_id}
)

# 3. 查看结果
result = analyze_resp.json()
print(f"\n情感: {result['emotion']['primary']}")
print(f"标签: {', '.join(result['tags'])}")
print(f"摘要: {result['description']['summary']}")
```

运行：`python my_test.py`

---

## ✅ 预期结果

成功的测试应该显示：

```
==================================================
  步骤 1: 上传文件
==================================================

ℹ️  上传文件: photo.jpg
✅ 上传成功！
ℹ️  Material ID: abc-123-def-456...
ℹ️  文件大小: 2456789 bytes
ℹ️  文件类型: image

==================================================
  步骤 2: AI分析
==================================================

ℹ️  开始分析 Material: abc-123-def-456...
⚠️  这可能需要10-30秒，请耐心等待...

✅ 分析完成！耗时: 18.3秒

==================================================
  步骤 3: 查看结果
==================================================

💭 情感分析
   主要情感: joy
   情感强度: 85.00%
   情感描述: 这张照片展现了欢乐的场景

🏷️ 标签生成
   所有标签: 朋友, 聚会, 餐厅, 笑容, 晚餐
   person: 朋友
   location: 餐厅
   activity: 聚会, 晚餐

📝 内容描述
   摘要: 朋友们在餐厅聚会用餐
   详细: 这是一张拍摄于餐厅的照片，画面中有几位朋友围坐在餐桌旁...

🔑 关键元素: 餐厅, 朋友, 笑容, 晚餐, 聚会

✅ 测试成功！所有功能正常工作
```

---

## 🐛 常见问题排查

### 问题1：连接后端失败

**错误：** `❌ 无法连接到后端服务 (http://localhost:8000)`

**解决方法：**
1. 检查后端是否已启动
2. 检查端口8000是否被占用
3. 尝试访问 http://localhost:8000/docs

### 问题2：API密钥错误

**错误：** `请设置VOLCENGINE_API_KEY环境变量`

**解决方法：**
1. 检查 `MVP/backend/.env` 文件是否存在
2. 确认API密钥格式正确（`ak-xxxxx`）
3. 重启后端服务

### 问题3：分析超时

**错误：** `❌ 分析过程出错: HTTPConnectionPool... Timeout`

**解决方法：**
1. 检查网络连接
2. 增加超时时间：在 `test_ai_analysis.py` 中修改 `timeout=120` 为更大的值
3. 确认API密钥有足够额度

### 问题4：文件类型不支持

**错误：** `❌ 上传失败 (状态码: 400)`

**解决方法：**
1. 确保文件类型在支持列表中
2. 支持的类型：image/*, video/*, audio/*, text/*
3. 检查文件MIME类型是否正确

### 问题5：数据库错误

**错误：** `❌ sqlite3.OperationalError: unable to open database file`

**解决方法：**
```bash
cd MVP/backend
mkdir -p data
alembic upgrade head
```

---

## 📊 性能参考

根据测试情况，AI分析时间参考：

| 文件类型 | 大小 | 分析时间 |
|---------|------|---------|
| 图片（jpg） | < 1MB | 10-20秒 |
| 图片（png） | 1-5MB | 15-30秒 |
| 图片（jpg） | > 5MB | 30-60秒 |
| 文本（txt） | < 10KB | 5-15秒 |
| 文本（md） | 10-100KB | 10-25秒 |

*注：实际时间取决于网络状况和API响应速度*

---

## 💡 测试技巧

1. **从小文件开始** - 先用小图片（<1MB）测试，快速验证功能
2. **使用缓存** - 重复分析同一文件会直接返回缓存结果
3. **查看日志** - 后端终端会显示详细日志，有助于调试
4. **批量测试** - 可以循环测试多个文件

批量测试示例：

```bash
# 测试多张图片
for photo in test-photos/*.jpg; do
    echo "Testing $photo..."
    python test_ai_analysis.py --photo "$photo"
done
```

---

## 🎯 下一步

测试成功后，你可以：

1. **集成到前端** - 在前端调用这些API
2. **查看文档** - 了解更多API端点
3. **继续开发** - 实现Level 2功能（材料关系构建）

---

**有问题？** 查看主文档：[README.md](../../README.md)
