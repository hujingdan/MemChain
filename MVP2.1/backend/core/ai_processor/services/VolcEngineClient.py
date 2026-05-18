"""
火山方舟AI客户端

负责与火山方舟平台API交互，支持DeepSeek v3等模型
"""

import os
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from enum import Enum
import json
import base64

from config.development import get_settings

settings = get_settings()


class ModelType(str, Enum):
    """支持的AI模型类型"""
    DEEPSEEK_V3 = "deepseek-v3"  # DeepSeek V3（通用）
    DEEPSEEK_V3_LITE = "deepseek-v3-lite"  # DeepSeek V3 Lite（快速）


class RoleType(str, Enum):
    """消息角色类型"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class VolcEngineClient:
    """火山方舟API客户端"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        初始化火山方舟客户端

        Args:
            api_key: API密钥（默认从环境变量VOLCENGINE_API_KEY读取）
            endpoint: API端点（默认使用北京区域）
            model: 默认模型（默认使用deepseek-v3）
        """
        self.api_key = api_key or os.getenv("VOLCENGINE_API_KEY", settings.VOLCENGINE_API_KEY)
        self.endpoint = endpoint or settings.VOLCENGINE_ENDPOINT
        self.model = model or settings.DEFAULT_MODEL
        self.timeout = settings.AI_TIMEOUT
        self.max_retries = settings.AI_MAX_RETRIES

        if not self.api_key or self.api_key == "your-volcengine-api-key":
            raise ValueError(
                "请设置VOLCENGINE_API_KEY环境变量或在配置中设置有效的API密钥"
            )

    async def _make_request(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        发起API请求

        Args:
            messages: 消息列表
            model: 模型名称（覆盖默认模型）
            temperature: 温度参数（0-1，越高越随机）
            max_tokens: 最大token数
            **kwargs: 其他参数

        Returns:
            API响应数据
        """
        url = f"{self.endpoint}/chat/completions"
        model = model or self.model

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

        # 添加额外参数
        payload.update(kwargs)

        # 重试逻辑
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=self.timeout)
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            return data
                        else:
                            error_text = await response.text()
                            raise Exception(
                                f"API请求失败 (状态码: {response.status}): {error_text}"
                            )

            except asyncio.TimeoutError:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(1 * (attempt + 1))  # 指数退避
                    continue
                raise Exception(f"API请求超时（{self.timeout}秒）")
            except Exception as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(1 * (attempt + 1))
                    continue
                raise e

    async def chat(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        response_format: Optional[Dict[str, str]] = None
    ) -> str:
        """
        简单的对话接口

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            response_format: 响应格式，例如 {"type": "json_object"}

        Returns:
            AI回复文本
        """
        messages = []

        if system_prompt:
            messages.append({
                "role": RoleType.SYSTEM.value,
                "content": system_prompt
            })

        messages.append({
            "role": RoleType.USER.value,
            "content": prompt
        })

        kwargs = {}
        if response_format:
            kwargs["response_format"] = response_format

        response = await self._make_request(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

        # 提取回复内容
        return response["choices"][0]["message"]["content"]

    async def analyze_image(
        self,
        image_path: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        detail: str = "auto"
    ) -> str:
        """
        图像分析接口

        Args:
            image_path: 图片路径（本地路径或URL）
            prompt: 分析提示词
            system_prompt: 系统提示词（可选）
            model: 模型名称
            detail: 分析详细程度（low/high/auto）

        Returns:
            AI分析结果
        """
        messages = []

        if system_prompt:
            messages.append({
                "role": RoleType.SYSTEM.value,
                "content": system_prompt
            })

        # 读取图片并编码为base64
        if image_path.startswith(("http://", "https://")):
            # URL
            image_content = {
                "type": "image_url",
                "image_url": {"url": image_path}
            }
        else:
            # 本地文件
            with open(image_path, "rb") as f:
                image_data = f.read()
                image_base64 = base64.b64encode(image_data).decode("utf-8")
                image_content = {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }

        messages.append({
            "role": RoleType.USER.value,
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                image_content
            ]
        })

        response = await self._make_request(
            messages=messages,
            model=model
        )

        return response["choices"][0]["message"]["content"]

    async def analyze_text(
        self,
        text: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None
    ) -> str:
        """
        文本分析接口

        Args:
            text: 待分析文本
            prompt: 分析提示词
            system_prompt: 系统提示词
            model: 模型名称

        Returns:
            AI分析结果
        """
        messages = []

        if system_prompt:
            messages.append({
                "role": RoleType.SYSTEM.value,
                "content": system_prompt
            })

        # 将待分析文本和提示词结合
        full_prompt = f"{prompt}\n\n待分析文本：\n{text}"

        messages.append({
            "role": RoleType.USER.value,
            "content": full_prompt
        })

        response = await self._make_request(
            messages=messages,
            model=model
        )

        return response["choices"][0]["message"]["content"]

    def chat_sync(self, *args, **kwargs) -> str:
        """
        同步版本的chat接口（用于兼容性）

        注意：这只是异步版本的包装，会创建新的事件循环
        """
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 如果已有运行中的事件循环，使用create_task
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    asyncio.run,
                    self.chat(*args, **kwargs)
                )
                return future.result()
        else:
            return asyncio.run(self.chat(*args, **kwargs))


# 全局单例
_ai_client: Optional[VolcEngineClient] = None


def get_ai_client() -> VolcEngineClient:
    """获取AI客户端单例"""
    global _ai_client
    if _ai_client is None:
        _ai_client = VolcEngineClient()
    return _ai_client
