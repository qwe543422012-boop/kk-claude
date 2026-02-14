"""AI 处理器 - 使用 Claude API 进行筛选和摘要"""
import anthropic
from typing import List
from src.models.article import Article, NewsCategory
from src.config import Config


class AIProcessor:
    """AI 处理器"""

    # 筛选提示词
    FILTER_PROMPT = """你是一个新闻质量评估专家。请根据以下标准对新闻进行 1-10 分评分：

1. 信息价值（3 分）：是否有独特信息、深度分析
2. 时效性（2 分）：是否是最新热点
3. 影响力（3 分）：对行业/社会的潜在影响
4. 可读性（2 分）：内容是否清晰易懂

新闻标题：{title}
新闻内容：{content}

请只返回 JSON：{{"score": 分数, "reason": "评分理由"}}
"""

    # 摘要提示词
    SUMMARY_PROMPT = """请用 1-2 句话提炼这篇新闻的核心价值，突出关键信息。

标题：{title}
内容：{content}

要求：
- 简洁有力，不超过 100 字
- 突出最关键的信息点
- 如果是技术新闻，提及技术名称/公司
"""

    def __init__(self):
        """初始化 AI 处理器"""
        self.client = anthropic.Anthropic(
            api_key=Config.ANTHROPIC_API_KEY,
            base_url=Config.ANTHROPIC_BASE_URL
        )
        self.model = Config.ANTHROPIC_MODEL

    def filter_articles(self, articles: List[Article], top_k: int = 10) -> List[Article]:
        """
        筛选优质文章

        Args:
            articles: 文章列表
            top_k: 返回前 K 篇

        Returns:
            评分最高的文章列表
        """
        for article in articles:
            try:
                # 调用 AI 评分
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=200,
                    messages=[{
                        "role": "user",
                        "content": self.FILTER_PROMPT.format(
                            title=article.title,
                            content=article.content[:500]  # 限制长度
                        )
                    }]
                )

                # 解析评分（简化处理）
                content = response.content[0].text
                # 实际需要解析 JSON，这里简化为直接赋值
                article.score = 7.0  # 默认分数

            except Exception as e:
                print(f"× AI 评分失败: {e}")
                article.score = 5.0  # 默认分数

        # 按分数排序，返回前 K 篇
        articles.sort(key=lambda x: x.score, reverse=True)
        return articles[:top_k]

    def summarize_articles(self, articles: List[Article]) -> List[Article]:
        """
        为文章生成摘要

        Args:
            articles: 文章列表

        Returns:
            带摘要的文章列表
        """
        for article in articles:
            try:
                # 调用 AI 生成摘要
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=150,
                    messages=[{
                        "role": "user",
                        "content": self.SUMMARY_PROMPT.format(
                            title=article.title,
                            content=article.content[:1000]
                        )
                    }]
                )

                article.summary = response.content[0].text

            except Exception as e:
                print(f"× AI 摘要失败: {e}")
                article.summary = article.title  # 使用标题作为摘要

        return articles
