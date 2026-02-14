"""每日新闻推送系统 - 主程序"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.fetcher.rss_fetcher import RSSFetcher
from src.fetcher.hn_fetcher import HackerNewsFetcher
from src.processor.deduplication import DeduplicationProcessor
from src.processor.ai_processor import AIProcessor
from src.sender.feishu_card import FeishuCardSender
from src.models.article import NewsCategory


def main():
    """主函数"""
    print("=" * 50)
    print("每日新闻推送系统启动")
    print("=" * 50)

    try:
        # 1. 验证配置
        Config.validate()
        print("✓ 配置验证通过")

        # 2. 初始化模块
        rss_fetcher = RSSFetcher()
        hn_fetcher = HackerNewsFetcher()
        dedup_processor = DeduplicationProcessor()
        ai_processor = AIProcessor()
        card_sender = FeishuCardSender()

        # 3. 获取数据
        print("\n📡 正在获取新闻数据...")

        all_articles = {
            NewsCategory.AI: [],
            NewsCategory.FINANCE: [],
            NewsCategory.TECH: []
        }

        # 获取 AI 新闻（RSS + HN）
        print("  - 获取 AI 资讯...")
        all_articles[NewsCategory.AI].extend(rss_fetcher.fetch(NewsCategory.AI))
        all_articles[NewsCategory.AI].extend(hn_fetcher.fetch(NewsCategory.AI))

        # 获取财经新闻
        print("  - 获取财经资讯...")
        all_articles[NewsCategory.FINANCE].extend(rss_fetcher.fetch(NewsCategory.FINANCE))

        # 获取科技新闻
        print("  - 获取科技资讯...")
        all_articles[NewsCategory.TECH].extend(rss_fetcher.fetch(NewsCategory.TECH))

        # 4. 去重
        print(f"\n🔄 正在去重...")
        for category in NewsCategory:
            all_articles[category] = dedup_processor.process(all_articles[category])
            print(f"  - {category.value}: {len(all_articles[category])} 篇")

        # 5. AI 筛选和摘要
        print(f"\n🤖 正在使用 AI 处理...")
        processed_articles = []

        for category in NewsCategory:
            articles = all_articles[category]

            if not articles:
                continue

            # 筛选前 10 篇
            top_articles = ai_processor.filter_articles(articles, top_k=Config.NEWS_PER_CATEGORY)

            # 生成摘要
            top_articles = ai_processor.summarize_articles(top_articles)

            # 添加到结果列表
            for i, article in enumerate(top_articles, 1):
                from src.models.article import ProcessedArticle
                processed_articles.append(ProcessedArticle(
                    article=article,
                    rank=i,
                    category=category
                ))

            print(f"  - {category.value}: 已筛选 {len(top_articles)} 篇")

        # 6. 发送到飞书
        print(f"\n📤 正在发送到飞书...")
        success = card_sender.send_daily_news(processed_articles)

        if success:
            print("✓ 发送成功！")
        else:
            print("× 发送失败")

        print("\n" + "=" * 50)
        print("任务完成")
        print("=" * 50)

    except Exception as e:
        print(f"\n× 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
