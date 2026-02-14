"""数据获取基类"""
from abc import ABC, abstractmethod
from typing import List
from src.models.article import Article, NewsCategory


class BaseFetcher(ABC):
    """数据获取器基类"""

    @abstractmethod
    def fetch(self, category: NewsCategory, limit: int = 50) -> List[Article]:
        """
        获取新闻数据

        Args:
            category: 新闻分类
            limit: 最大获取数量

        Returns:
            文章列表
        """
        pass
