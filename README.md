# AI新词挖掘系统

![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Enabled-brightgreen)
![OpenAI](https://img.shields.io/badge/OpenAI-API-orange)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-Integration-blue)
![Python](https://img.shields.io/badge/Python-3.9+-blue)

通过GitHub Actions + OpenAI API + Google Sheets实现的零维护AI新词挖掘系统

## 🌟 核心功能

- **🕷️ 自动爬取**: 从toolify.ai抓取最新AI工具信息
- **🧠 AI分析**: 使用OpenAI API智能分析并提取AI新词术语
- **📊 数据处理**: 去重、分类和趋势分析
- **📋 自动更新**: 结果自动更新到Google Sheets
- **⏰ 定时执行**: 通过GitHub Actions实现零维护定时运行

## 🏗️ 系统流程

```
GitHub Actions (定时触发)
    ↓
🕷️ 爬取toolify.ai新工具
    ↓
🧠 OpenAI分析提取新词
    ↓
⚙️ 数据处理去重
    ↓
📊 更新Google Sheets
    ↓
🔔 发送完成通知
```

## 🚀 快速启动

### 1. 环境配置

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp env.example .env
# 编辑.env文件，添加API密钥
```

### 2. 配置说明

#### 必需的环境变量：
- `OPENAI_API_KEY`: OpenAI API密钥
- `GOOGLE_SHEETS_ID`: Google Sheets表格ID
- `GOOGLE_SHEETS_CREDENTIALS_PATH`: Google API凭据文件路径

#### 可选配置：
- `TARGET_URL`: 目标网站 (默认: https://www.toolify.ai/new)
- `NOTIFICATION_WEBHOOK_URL`: 通知Webhook URL
- `DEBUG_MODE`: 调试模式

### 3. 本地测试

```bash
# 运行完整流程
python main.py

# 调试模式
DEBUG_MODE=true python main.py
```

## ⚙️ GitHub Actions自动化

### 设置GitHub Secrets

在GitHub仓库 Settings > Secrets and variables > Actions 中添加：

- `OPENAI_API_KEY`: 你的OpenAI API密钥
- `GOOGLE_SHEETS_ID`: Google Sheets表格ID
- `GOOGLE_SHEETS_CREDENTIALS`: Google API凭据JSON内容
- `GOOGLE_SHEETS_RANGE`: 数据范围 (默认: Sheet1!A:Z)

### 定时任务

系统默认每天上午6点(UTC)自动运行，也可以手动触发。

## 📊 输出格式

### Google Sheets结构
| 列名 | 描述 |
|------|------|
| Word | 提取的新词/术语 |
| Category | 词汇分类 |
| Definition | 词汇定义 |
| Importance | 重要性级别 |
| Trend Potential | 趋势潜力评分 |
| Business Value | 商业价值 |
| Is Emerging | 是否为新兴术语 |

## 🎯 项目结构

```
AI new words/
├── main.py                 # 主程序
├── config.py              # 配置管理
├── requirements.txt       # 依赖包
├── env.example           # 环境变量示例
├── .github/workflows/    # GitHub Actions配置
│   └── ai-words-mining-simple.yml
└── src/                  # 核心模块
    ├── toolify_scraper.py       # 网页爬虫
    ├── openai_analyzer.py       # AI分析
    ├── google_sheets_integration.py  # Google Sheets集成
    ├── data_processor.py        # 数据处理
    └── notification_system.py   # 通知系统
```

## 🔧 核心模块

### 1. 网页爬虫 (`toolify_scraper.py`)
- 从toolify.ai抓取最新AI工具
- 支持动态内容加载
- 智能错误处理

### 2. AI分析 (`openai_analyzer.py`)
- 使用OpenAI API分析工具描述
- 智能提取新词和术语
- 批量处理优化

### 3. 数据处理 (`data_processor.py`)
- 去重和分类
- 趋势分析
- 评分排序

### 4. Google Sheets集成 (`google_sheets_integration.py`)
- 自动更新表格
- 数据格式化
- 错误恢复

## 🆘 常见问题

### Q: 如何获取Google Sheets API凭据？
A: 
1. 访问Google Cloud Console
2. 创建项目并启用Google Sheets API
3. 创建服务账户
4. 下载JSON凭据文件

### Q: 如何设置定时任务？
A: 修改`.github/workflows/ai-words-mining-simple.yml`中的cron表达式

### Q: 如何处理API配额限制？
A: 调整`config.py`中的`BATCH_SIZE`和`SCRAPING_DELAY`参数

## 📄 许可证

本项目使用MIT许可证。

---

**⭐ 如果这个项目对你有帮助，请给个Star！** 