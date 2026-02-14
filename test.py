"""快速测试版本 - 只处理少量新闻"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.fetcher.rss_fetcher import RSSFetcher
from src.processor.ai_processor import AIProcessor
from src.sender.feishu_card import FeishuCardSender
from src.models.article import NewsCategory, ProcessedArticle

def main():
    """测试主函数"""
    print("=" * 50)
    print("快速测试版本")
    print("=" * 50)

    # 1. 获取数据（只获取 3 条）
    print("\n📡 正在获取数据...")
    rss_fetcher = RSSFetcher()

    test_articles = {
        NewsCategory.AI: rss_fetcher.fetch(NewsCategory.AI, limit=3),
        NewsCategory.FINANCE: rss_fetcher.fetch(NewsCategory.FINANCE, limit=3),
        NewsCategory.TECH: rss_fetcher.fetch(NewsCategory.TECH, limit=3),
    }

    for category, articles in test_articles.items():
        print(f"  - {category.value}: {len(articles)} 篇")

    # 2. AI 处理（只处理前 1 条）
    print("\n🤖 正在使用 AI 处理...")
    ai_processor = AIProcessor()

    processed_articles = []

    for category, articles in test_articles.items():
        if not articles:
            continue

        # 只取前 1 条
        top_articles = [articles[0]]
        top_articles = ai_processor.summarize_articles(top_articles)

        processed_articles.append(ProcessedArticle(
            article=top_articles[0],
            rank=1,
            category=category
        ))

        print(f"  - {category.value}: 已处理 1 篇")

    # 3. 发送到飞书
    print("\n📤 正在发送到飞书...")
    card_sender = FeishuCardSender()

    success = card_sender.send_daily_news(processed_articles)

    if success:
        print("✓ 发送成功！")
    else:
        print("× 发送失败")

    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == "__main__":
    main()
