"""配置管理"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 加载 .env 文件
load_dotenv(BASE_DIR / ".env")


class Config:
    """系统配置"""

    # 飞书配置
    FEISHU_WEBHOOK = os.getenv("FEISHU_WEBHOOK")

    # Claude API 配置
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

    # 系统配置
    NEWS_PER_CATEGORY = int(os.getenv("NEWS_PER_CATEGORY", "10"))
    SCHEDULE_TIME = os.getenv("SCHEDULE_TIME", "10:00")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # 数据目录
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"

    @classmethod
    def validate(cls):
        """验证配置"""
        if not cls.FEISHU_WEBHOOK:
            raise ValueError("缺少飞书 Webhook 配置")
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("缺少 Claude API Key 配置")

        # 确保目录存在
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
