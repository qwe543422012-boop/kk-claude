# 每日新闻推送系统

自动从各优质数据源搜寻 AI、财经、科技新闻，通过 AI 筛选出最优质内容，每天 10 点自动推送到飞书。

## 功能特点

- **多源聚合**：支持 RSS、API 多种数据源
- **AI 筛选**：使用 Claude API 进行质量评分
- **智能摘要**：自动生成新闻摘要
- **飞书推送**：精美的消息卡片格式
- **定时任务**：支持 crontab 定时运行

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置

编辑 `.env` 文件，填入你的配置：

```bash
# 飞书配置
FEISHU_WEBHOOK=https://open.feishu.cn/open-apis/bot/v2/hook/xxx

# Claude API 配置
ANTHROPIC_API_KEY=your_api_key
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
ANTHROPIC_MODEL=glm-4.7

# 系统配置
NEWS_PER_CATEGORY=10
```

### 3. 运行

```bash
python run.py
```

### 4. 配置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天 10:00 运行）
0 10 * * * cd /Users/mac/Desktop/claudecode项目/每日新闻推送系统 && /usr/local/bin/python3 run.py >> logs/cron.log 2>&1
```

## 项目结构

```
每日新闻推送系统/
├── src/
│   ├── fetcher/         # 数据获取模块
│   ├── processor/       # AI 处理模块
│   ├── sender/          # 飞书推送模块
│   ├── models/          # 数据模型
│   └── config.py       # 配置管理
├── data/              # 数据目录
├── logs/              # 日志目录
├── run.py            # 主程序
├── .env              # 配置文件
└── requirements.txt    # 依赖
```

## 数据源

| 分类 | 数据源 |
|------|--------|
| AI 资讯 | arXiv CS.AI, MIT Tech Review, Hacker News |
| 财经资讯 | 财新网, FT 中文 |
| 科技资讯 | 36氪, The Verge |
