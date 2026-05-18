"""
InsightService.py - AI洞察服务（极简版）
对上传的图片进行分析：提取主色调、计算亮度、生成标签。
不需要深度学习模型，用PIL实现即可体现AI分析思路。
"""
from pathlib import Path
from typing import Optional, Dict
from PIL import Image
import colorsys


class InsightService:
    """
    图片AI分析服务。
    所有方法均为类方法，无状态，接收图片路径返回分析结果。
    """

    @classmethod
    def analyze_image(cls, image_path: str) -> Optional[Dict]:
        """
        分析单张图片，返回AI分析结果。
        
        参数:
            image_path: 图片文件的完整路径
        
        返回:
            分析结果字典，包含主色调、亮度、标签等；非图片返回None
        """
        path = Path(image_path)
        if not path.exists():
            return None

        # 只处理图片文件
        mime_guess = cls._guess_mime(path)
        if not mime_guess.startswith("image/"):
            return None

        try:
            with Image.open(path) as img:
                # 转换为RGB模式（处理PNG的RGBA、GIF的P模式等）
                img_rgb = img.convert("RGB")

                # 1. 提取主色调（颜色量化取前3）
                dominant_colors = cls._extract_dominant_colors(img_rgb, n=3)

                # 2. 计算平均亮度
                avg_brightness = cls._calculate_brightness(img_rgb)

                # 3. 生成标签
                tag = cls._generate_tag(avg_brightness, dominant_colors)

                return {
                    "dominant_colors": dominant_colors,   # 主色调列表 [R,G,B]
                    "brightness": round(avg_brightness, 2),  # 平均亮度 0-255
                    "brightness_level": cls._brightness_level(avg_brightness),  # 文字描述
                    "ai_tag": tag,                         # AI生成标签
                    "width": img.width,                    # 图片宽度
                    "height": img.height,                  # 图片高度
                    "aspect_ratio": round(img.width / img.height, 2),  # 宽高比
                }
        except Exception as e:
            print(f"[AI分析失败] {path}: {e}")
            return None

    @classmethod
    def _extract_dominant_colors(cls, img: Image.Image, n: int = 3) -> list:
        """
        提取图片的主色调。
        方法：缩小图片 -> 颜色量化 -> 取出现频率最高的n种颜色。
        
        返回: [[R,G,B], [R,G,B], ...]
        """
        # 缩小图片加速计算
        small = img.copy()
        small.thumbnail((150, 150))  # 最大150x150，保持比例

        # 量化到n种颜色
        quantized = small.quantize(colors=n, method=Image.Quantize.MEDIANCUT)

        # 获取调色板
        palette = quantized.getpalette()[:n * 3]  # 前n种颜色的RGB值

        colors = []
        for i in range(n):
            r = palette[i * 3]
            g = palette[i * 3 + 1]
            b = palette[i * 3 + 2]
            colors.append([r, g, b])

        return colors

    @classmethod
    def _calculate_brightness(cls, img: Image.Image) -> float:
        """
        计算图片平均亮度（0-255）。
        方法：缩小后采样计算，避免遍历所有像素。
        """
        small = img.copy()
        small.thumbnail((100, 100))

        pixels = list(small.getdata())
        if not pixels:
            return 0.0

        total = 0
        for r, g, b in pixels:
            # 感知亮度公式：人眼对绿色最敏感，蓝色最不敏感
            total += (0.299 * r + 0.587 * g + 0.114 * b)

        return total / len(pixels)

    @classmethod
    def _brightness_level(cls, brightness: float) -> str:
        """将亮度值转为文字描述。"""
        if brightness > 180:
            return "明亮"
        elif brightness > 100:
            return "适中"
        else:
            return "偏暗"

    @classmethod
    def _generate_tag(cls, brightness: float, colors: list) -> str:
        """
        根据亮度和主色调生成简单标签。
        这是一个极简的"规则引擎"，后续可替换为真正的AI模型。
        """
        # 判断色调倾向
        avg_r = sum(c[0] for c in colors) / len(colors)
        avg_g = sum(c[1] for c in colors) / len(colors)
        avg_b = sum(c[2] for c in colors) / len(colors)

        # 找出主导色通道
        max_channel = max(avg_r, avg_g, avg_b)
        hue_desc = ""
        if max_channel == avg_r and avg_r > avg_g + 20 and avg_r > avg_b + 20:
            hue_desc = "暖色调"
        elif max_channel == avg_b and avg_b > avg_r + 20 and avg_b > avg_g + 20:
            hue_desc = "冷色调"
        elif avg_g > avg_r + 10 and avg_g > avg_b + 10:
            hue_desc = "自然绿调"
        else:
            hue_desc = "中性色调"

        # 结合亮度生成标签
        level = cls._brightness_level(brightness)
        return f"{level}的{hue_desc}照片"

    @classmethod
    def _guess_mime(cls, path: Path) -> str:
        """根据扩展名猜测MIME类型。"""
        ext = path.suffix.lower()
        mime_map = {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".gif": "image/gif",
            ".bmp": "image/bmp", ".webp": "image/webp",
            ".mp3": "audio/mpeg", ".wav": "audio/wav",
            ".txt": "text/plain", ".pdf": "application/pdf",
        }
        return mime_map.get(ext, "application/octet-stream")