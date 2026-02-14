"""飞书卡片推送"""
from src.feishu_bot import FeishuBot
from typing import List
from datetime import datetime
from src.models.article import Article, ProcessedArticle, NewsCategory
from src.config import Config


class FeishuCardSender:
    """飞书卡片推送器"""

    # 分类名称映射
    CATEGORY_NAMES = {
        NewsCategory.AI: "🤖 AI 资讯",
        NewsCategory.FINANCE: "💰 财经资讯",
        NewsCategory.TECH: "💻 科技资讯"
    }

    def __init__(self):
        """初始化"""
        self.bot = FeishuBot(Config.FEISHU_WEBHOOK)

    def send_daily_news(self, articles: List[ProcessedArticle]) -> bool:
        """
        发送每日新闻卡片

        Args:
            articles: 处理后的文章列表（已按分类和排名排序）

        Returns:
            是否发送成功
        """
        # 按分类整理
        categorized = {
            NewsCategory.AI: [],
            NewsCategory.FINANCE: [],
            NewsCategory.TECH: []
        }

        for item in articles:
            categorized[item.category].append(item)

        # 构建卡片内容
        card = self._build_card(categorized)

        # 发送
        try:
            result = self.bot.send_card(card)
            return result.get("success", False)
        except Exception as e:
            print(f"× 发送飞书消息失败: {e}")
            return False

    def _build_card(self, categorized: dict) -> dict:
        """构建飞书消息卡片"""
        elements = []

        # 标题和日期
        today = datetime.now().strftime("%Y-%m-%d")
        weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][datetime.now().weekday()]

        elements.append({
            "tag": "div",
            "text": {
                "content": f"📰 每日科技资讯日报 | {today} {weekday}",
                "tag": "lark_md"
            }
        })

        # 每个分类
        for category, articles in categorized.items():
            if not articles:
                continue

            # 分类标题
            elements.append({
                "tag": "hr"
            })

            elements.append({
                "tag": "div",
                "text": {
                    "content": f"**{self.CATEGORY_NAMES[category]}（Top {len(articles)}）**",
                    "tag": "lark_md"
                }
            })

            # 文章列表
            for i, item in enumerate(articles[:10], 1):
                article = item.article
                summary = article.summary or article.title

                elements.append({
                    "tag": "div",
                    "text": {
                        "content": f"{i}. **{article.title}**\n   ▸ {summary}\n   ▸ {article.url}",
                        "tag": "lark_md"
                    }
                })

        # 底部信息
        total = sum(len(articles) for articles in categorized.values())
        elements.append({"tag": "hr"})
        elements.append({
            "tag": "div",
            "text": {
                "content": f"⚡ 今日处理：{total} 篇 | 📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                "tag": "lark_md"
            }
        })

        # 构建卡片
        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"content": "每日科技资讯", "tag": "plain_text"},
                "template": "blue"
            },
            "elements": elements
        }

        return card
