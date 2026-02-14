"""新闻文章数据模型"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class NewsCategory(Enum):
    """新闻分类"""
    AI = "ai"
    FINANCE = "finance"
    TECH = "tech"


@dataclass
class Article:
    """文章数据模型"""
    title: str
    url: str
    content: str
    category: NewsCategory
    source: str
    published_at: Optional[datetime] = None
    author: Optional[str] = None
    score: float = 0.0  # AI 评分
    summary: Optional[str] = None  # AI 摘要

    def __hash__(self):
        """用于去重的哈希值"""
        return hash(self.url)

    def __eq__(self, other):
        """用于去重的比较"""
        if not isinstance(other, Article):
            return False
        return self.url == other.url


@dataclass
class ProcessedArticle:
    """处理后的文章"""
    article: Article
    rank: int  # 排名
    category: NewsCategory
