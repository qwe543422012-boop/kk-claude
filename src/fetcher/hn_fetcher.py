"""Hacker News API 数据获取器"""
import httpx
from typing import List
from datetime import datetime
from src.models.article import Article, NewsCategory
from src.fetcher.base import BaseFetcher


class HackerNewsFetcher(BaseFetcher):
    """Hacker News API 数据获取器"""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout, base_url="https://hacker-news.firebaseio.com/v0")

    def fetch(self, category: NewsCategory, limit: int = 50) -> List[Article]:
        """获取 Hacker News 头条"""
        articles = []

        try:
            # 获取头条列表
            response = self.client.get("/topstories.json")
            story_ids = response.json()[:limit]

            for story_id in story_ids:
                try:
                    # 获取每条详情
                    story_response = self.client.get(f"/item/{story_id}.json")
                    story = story_response.json()

                    # 过滤非 AI 相关的新闻
                    if not self._is_ai_related(story.get("title", "")):
                        continue

                    # 解析时间
                    published_at = None
                    if story.get("time"):
                        published_at = datetime.fromtimestamp(story["time"])

                    article = Article(
                        title=story.get("title", ""),
                        url=story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                        content=story.get("text", ""),
                        category=NewsCategory.AI,
                        source="Hacker News",
                        published_at=published_at
                    )
                    articles.append(article)

                except Exception as e:
                    print(f"× 获取故事 {story_id} 失败: {e}")
                    continue

        except Exception as e:
            print(f"× 获取 Hacker News 失败: {e}")

        return articles

    def _is_ai_related(self, title: str) -> bool:
        """判断是否与 AI 相关"""
        ai_keywords = [
            "AI", "artificial intelligence", "machine learning",
            "deep learning", "neural network", "GPT", "LLM",
            "人工智能", "机器学习", "深度学习"
        ]
        title_lower = title.lower()
        return any(keyword.lower() in title_lower for keyword in ai_keywords)

    def __del__(self):
        """清理资源"""
        if hasattr(self, 'client'):
            self.client.close()
