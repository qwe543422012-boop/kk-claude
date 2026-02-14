"""去重处理器"""
from typing import List
from src.models.article import Article


class DeduplicationProcessor:
    """去重处理器"""

    def __init__(self, similarity_threshold: float = 0.85):
        """
        Args:
            similarity_threshold: 相似度阈值（0-1）
        """
        self.similarity_threshold = similarity_threshold

    def process(self, articles: List[Article]) -> List[Article]:
        """
        去除重复文章

        Args:
            articles: 文章列表

        Returns:
            去重后的文章列表
        """
        seen_urls = set()
        unique_articles = []

        for article in articles:
            # URL 去重
            if article.url in seen_urls:
                continue

            # 标题去重（简单版本）
            is_duplicate = False
            for seen_article in unique_articles:
                if self._is_similar(article.title, seen_article.title):
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_articles.append(article)
                seen_urls.add(article.url)

        return unique_articles

    def _is_similar(self, title1: str, title2: str) -> bool:
        """判断两个标题是否相似"""
        # 简化版本：检查包含关系
        title1_lower = title1.lower()
        title2_lower = title2.lower()

        # 如果一个标题包含另一个，认为相似
        return (title1_lower in title2_lower or
                title2_lower in title1_lower)
