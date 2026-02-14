#!/usr/bin/env python3
"""
飞书机器人 Webhook 消息推送工具
支持发送文本、富文本、消息卡片等多种格式
"""

import json
import hashlib
import hmac
import base64
import time
from typing import Optional
from urllib.parse import quote

import requests


class FeishuBot:
    """飞书自定义机器人客户端"""

    def __init__(self, webhook_url: str, sign_key: Optional[str] = None):
        """
        初始化飞书机器人

        Args:
            webhook_url: 飞书机器人 Webhook 地址
            sign_key: 签名密钥（如果启用了签名验证）
        """
        self.webhook_url = webhook_url
        self.sign_key = sign_key

    def _generate_sign(self, timestamp: int) -> str:
        """生成签名"""
        if not self.sign_key:
            return ""

        string_to_sign = f"{timestamp}\n{self.sign_key}"
        hmac_code = hmac.new(
            self.sign_key.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256
        ).digest()

        sign = base64.b64encode(hmac_code).decode("utf-8")
        return quote(sign)

    def _build_url(self) -> str:
        """构建带签名的请求 URL"""
        if not self.sign_key:
            return self.webhook_url

        timestamp = int(time.time())
        sign = self._generate_sign(timestamp)
        return f"{self.webhook_url}&timestamp={timestamp}&sign={sign}"

    def send_text(self, content: str, at_all: bool = False, at_mobiles: list = None) -> dict:
        """
        发送文本消息

        Args:
            content: 文本内容
            at_all: 是否 @所有人
            at_mobiles: 要 @的手机号列表

        Returns:
            响应结果
        """
        data = {
            "msg_type": "text",
            "content": {
                "text": content
            }
        }

        if at_all or at_mobiles:
            data["content"]["at"] = {}
            if at_all:
                data["content"]["at"]["atAll"] = True
            if at_mobiles:
                data["content"]["at"]["atMobiles"] = at_mobiles

        return self._send(data)

    def send_post(self, title: str, content: list) -> dict:
        """
        发送富文本消息

        Args:
            title: 消息标题
            content: 富文本内容列表，每个元素包含 tag、text 等字段

        Returns:
            响应结果
        """
        data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": content
                    }
                }
            }
        }
        return self._send(data)

    def send_card(self, card: dict) -> dict:
        """
        发送消息卡片

        Args:
            card: 消息卡片内容（JSON 格式）

        Returns:
            响应结果
        """
        data = {
            "msg_type": "interactive",
            "card": card
        }
        return self._send(data)

    def send_image(self, image_key: str) -> dict:
        """
        发送图片消息

        Args:
            image_key: 图片的 key（需要先上传图片获取）

        Returns:
            响应结果
        """
        data = {
            "msg_type": "image",
            "content": {
                "image_key": image_key
            }
        }
        return self._send(data)

    def _send(self, data: dict) -> dict:
        """
        发送 HTTP 请求

        Args:
            data: 要发送的数据

        Returns:
            响应结果
        """
        url = self._build_url()
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            result = response.json()
            if result.get("code") != 0:
                return {"success": False, "error": result.get("msg", "Unknown error")}
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
