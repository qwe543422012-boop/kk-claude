"""RSS 数据获取器"""
import feedparser
import httpx
from typing import List
from datetime import datetime
from src.models.article import Article, NewsCategory
from src.fetcher.base import BaseFetcher


class RSSFetcher(BaseFetcher):
    """RSS 数据获取器"""

    # RSS 源配置
    SOURCES = {
        NewsCategory.AI: [
            {
                "name": "arXiv CS.AI",
                "url": "http://export.arxiv.org/rss/cs.AI"
            },
            {
                "name": "MIT Tech Review AI",
                "url": "https://www.technologyreview.com/feed/?post_type=tops"
            }
        ],
        NewsCategory.FINANCE: [
            {
                "name": "财新网",
                "url": "https://www.caixin.com/rss/finance.xml"
            },
            {
                "name": "FT 中文",
                "url": "https://www.ftchinese.com/rss/feed"
            }
        ],
        NewsCategory.TECH: [
            {
                "name": "36氪",
                "url": "https://36kr.com/feed"
            },
            {
                "name": "The Verge",
                "url": "https://www.theverge.com/rss/index.xml"
            }
        ]
    }

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout)

    def fetch(self, category: NewsCategory, limit: int = 50) -> List[Article]:
        """获取 RSS 新闻"""
        articles = []
        sources = self.SOURCES.get(category, [])

        for source in sources:
            try:
                feed = feedparser.parse(source["url"])
                for entry in feed.entries[:limit]:
                    # 解析发布时间
                    published_at = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published_at = datetime(*entry.published_parsed[:6])

                    # 获取内容
                    content = ""
                    if hasattr(entry, 'description'):
                        content = entry.description
                    elif hasattr(entry, 'summary'):
                        content = entry.summary

                    article = Article(
                        title=entry.title,
                        url=entry.link,
                        content=content,
                        category=category,
                        source=source["name"],
                        published_at=published_at
                    )
                    articles.append(article)

            except Exception as e:
                print(f"× 获取 {source['name']} 失败: {e}")
                continue

        return articles

    def __del__(self):
        """清理资源"""
        if hasattr(self, 'client'):
            self.client.close()
