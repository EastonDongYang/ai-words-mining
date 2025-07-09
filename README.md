# AI Words Mining System

![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Enabled-brightgreen)
![OpenAI](https://img.shields.io/badge/OpenAI-API-orange)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-Integration-blue)
![Python](https://img.shields.io/badge/Python-3.9+-blue)

零维护的智能AI新词挖掘系统：GitHub Actions + OpenAI API + Google Sheets

## 🌟 系统特色

- **🤖 智能分析**: 使用OpenAI API分析AI工具并提取新词和趋势术语
- **🕷️ 自动爬取**: 自动从theresanaiforthat.com抓取最新AI工具信息
- **📊 数据处理**: 智能去重、分类排序和趋势分析
- **📋 自动更新**: 自动更新Google Sheets表格，生成可视化报告
- **🔔 智能通知**: 完成后发送详细的执行报告通知
- **⏰ 定时执行**: 通过GitHub Actions实现零维护的定时运行
- **🛠️ 高度可配置**: 支持多种配置选项和自定义参数

## 🏗️ 系统架构

```
GitHub Actions (定时触发)
    ↓
🕷️ 爬取AI工具数据 (theresanaiforthat.com)
    ↓
🧠 OpenAI API分析提取新词
    ↓
⚙️ 汇总去重处理
    ↓
📊 自动更新Google Sheets
    ↓
🔔 发送完成通知
```

## 📋 功能列表

### 核心功能
- ✅ 网页数据爬取（支持动态内容）
- ✅ OpenAI智能分析和新词提取
- ✅ 数据去重和趋势分析
- ✅ Google Sheets自动更新
- ✅ 多种通知方式（Webhook、邮件）
- ✅ GitHub Actions自动化

### 高级功能
- ✅ 智能词汇过滤和排序
- ✅ 趋势潜力评估
- ✅ 商业价值分析
- ✅ 多类别数据统计
- ✅ CSV导出功能
- ✅ 错误处理和重试机制

## 🚀 快速开始

### 1. 环境要求

- Python 3.9+
- OpenAI API密钥
- Google Sheets API凭据
- GitHub仓库（用于Actions）

### 2. 本地安装

```bash
# 克隆仓库
git clone https://github.com/你的用户名/ai-words-mining.git
cd ai-words-mining

# 安装依赖
# ⚠️ 重要：如果你的系统有多个Python版本，请使用以下命令
py -3.11 -m pip install -r requirements.txt

# 或者使用默认pip（如果只有一个Python版本）
pip install -r requirements.txt

# 复制配置文件
cp env.example .env

# 编辑配置文件
nano .env
```

### 3. 配置设置

#### 环境变量配置 (.env)

```bash
# OpenAI API配置
OPENAI_API_KEY=your_openai_api_key

# Google Sheets配置
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json
GOOGLE_SHEETS_ID=your_google_sheets_id
GOOGLE_SHEETS_RANGE=Sheet1!A:Z

# 爬取配置
TARGET_URL=https://theresanaiforthat.com/trending/week/top-50/?pos=1
SCRAPING_DELAY=2

# 通知配置
NOTIFICATION_WEBHOOK_URL=your_webhook_url_here
NOTIFICATION_EMAIL=your_email_here

# 系统配置
MAX_RETRIES=3
BATCH_SIZE=10
DEBUG_MODE=false
```

#### Google Sheets API设置

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用Google Sheets API
4. 创建服务账户凭据
5. 下载JSON凭据文件并重命名为 `credentials.json`
6. 将服务账户邮箱添加到你的Google Sheets编辑权限

#### OpenAI API设置

1. 访问 [OpenAI API页面](https://platform.openai.com/api-keys)
2. 创建新的API密钥
3. 将密钥添加到环境变量

### 4. 本地测试

```bash
# 🎯 推荐方式：使用批处理文件
run_test.bat    # 运行系统测试
run_system.bat  # 运行完整系统

# 或者手动指定Python版本（如果有多个Python版本）
py -3.11 test_system.py  # 运行测试
py -3.11 main.py         # 运行主程序

# 传统方式（单Python版本系统）
python test_system.py
python main.py

# 调试模式运行
DEBUG_MODE=true py -3.11 main.py
```

## ⚙️ GitHub Actions配置

### 1. GitHub Secrets设置

在你的GitHub仓库中，前往 `Settings` > `Secrets and variables` > `Actions`，添加以下secrets：

```
OPENAI_API_KEY=your_openai_api_key
GOOGLE_SHEETS_ID=your_google_sheets_id
GOOGLE_SHEETS_CREDENTIALS={"type":"service_account",...}
NOTIFICATION_WEBHOOK_URL=your_webhook_url
TARGET_URL=https://theresanaiforthat.com/trending/week/top-50/?pos=1
```

### 2. 定时任务配置

默认配置为每天上午6点（UTC）运行：

```yaml
schedule:
  - cron: '0 6 * * *'  # 每天6:00 AM UTC
```

你可以根据需要调整时间：
- `0 12 * * *` - 每天中午12点
- `0 6 * * 1` - 每周一上午6点
- `0 6 1 * *` - 每月1号上午6点

### 3. 手动触发

你也可以在GitHub Actions页面手动触发工作流程，并选择是否启用调试模式或测试模式。

## 📊 输出格式

### Google Sheets表格结构

| 列名 | 描述 |
|------|------|
| Word | 提取的新词/术语 |
| Category | 词汇分类 |
| Definition | 词汇定义 |
| Importance | 重要性级别 |
| Trend Potential | 趋势潜力评分 |
| Business Value | 商业价值 |
| Is Emerging | 是否为新兴术语 |
| Extraction Count | 提取次数 |
| Ranking Score | 排名得分 |
| First Seen | 首次发现时间 |
| Last Seen | 最后发现时间 |
| Related Terms | 相关术语 |
| Target Sectors | 目标行业 |
| Contexts | 上下文信息 |

### 通知格式

成功通知示例：
```
🎉 AI Words Mining System - Success Report

⏰ Completed: 2024-01-15 06:30:15

📊 Summary:
• Total Words Extracted: 42
• Emerging Terms: 15
• Average Trend Score: 7.5
• Categories: 8

🏆 Top Categories:
• AI Model: 12 words
• Technology: 8 words
• Methodology: 6 words

🔥 Top 5 Words:
1. RAG (AI Technique)
2. Multimodal (AI Capability)
3. Constitutional AI (AI Safety)
4. RLHF (Training Method)
5. Chain-of-Thought (Reasoning)

📋 View Full Report: https://docs.google.com/spreadsheets/d/...
```

## 🔧 高级配置

### 自定义爬取目标

你可以修改 `TARGET_URL` 来爬取不同的页面：

```bash
# 爬取不同时间段的数据
TARGET_URL=https://theresanaiforthat.com/trending/month/top-50/?pos=1

# 爬取特定分类
TARGET_URL=https://theresanaiforthat.com/category/image-generation/
```

### 调整分析参数

在 `config.py` 中可以调整以下参数：

```python
# 批处理大小（影响API调用频率）
BATCH_SIZE=10

# 最大重试次数
MAX_RETRIES=3

# 爬取延迟（秒）
SCRAPING_DELAY=2
```

### 自定义通知

你可以配置多种通知方式：

1. **Slack通知**: 使用Slack Webhook URL
2. **Discord通知**: 使用Discord Webhook URL
3. **邮件通知**: 配置SMTP设置
4. **自定义Webhook**: 发送到任何支持JSON的API

## 🛠️ 故障排除

### 常见问题

1. **Google Sheets权限错误**
   - 确保服务账户有表格编辑权限
   - 检查凭据文件格式是否正确

2. **OpenAI API限制**
   - 检查API密钥是否有效
   - 确认账户有足够的配额

3. **爬取失败**
   - 检查网络连接
   - 尝试降低爬取频率
   - 检查目标网站结构是否变化

4. **GitHub Actions失败**
   - 检查所有Secrets是否正确设置
   - 查看Actions日志获取详细错误信息

### 调试模式

启用调试模式获取更多信息：

```bash
DEBUG_MODE=true python main.py
```

调试模式会：
- 输出详细的执行日志
- 保存中间数据文件
- 显示配置信息
- 提供更多错误详情

## 📈 性能优化

### 建议设置

1. **API调用优化**
   - 合理设置 `BATCH_SIZE` (建议10-20)
   - 使用 `gpt-4o-mini` 模型平衡成本和质量

2. **爬取优化**
   - 适当增加 `SCRAPING_DELAY` 避免被限制
   - 使用合适的User-Agent

3. **数据处理优化**
   - 定期清理历史数据
   - 使用CSV导出进行本地分析

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

本项目使用MIT许可证。详情请见 [LICENSE](LICENSE) 文件。

## 🆘 支持

如果你遇到问题或有建议：

1. 查看 [Issues](https://github.com/你的用户名/ai-words-mining/issues)
2. 创建新Issue描述问题
3. 加入讨论区域

## 📊 数据使用说明

本系统从公开网站抓取数据，请遵守：

1. 网站使用条款
2. 数据使用规范
3. 隐私保护要求
4. 学术/商业使用限制

## 🔮 未来计划

- [ ] 支持更多数据源
- [ ] 添加情感分析功能
- [ ] 实现趋势预测
- [ ] 增加可视化图表
- [ ] 支持多语言分析
- [ ] 添加API接口

---

**⭐ 如果这个项目对你有帮助，请给个Star！** 