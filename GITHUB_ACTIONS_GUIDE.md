# GitHub Actions 运行指南

## 📋 问题分析

在GitHub Actions环境中运行时，系统可能会遇到以下问题：

1. **爬虫问题**：Selenium webdriver在Linux环境中可能无法正常工作
2. **网络限制**：可能无法访问外部网站进行爬取
3. **Google Sheets连接**：需要正确的credentials配置
4. **OpenAI API**：需要有效的API密钥

## 🔧 解决方案

### 1. 模拟数据模式

系统现在包含了一个模拟数据模块（`src/mock_web_scraper.py`），当真实爬虫失败时会自动启用：

```python
# 当主爬虫失败时，系统会自动调用
from src.mock_web_scraper import MockWebScraper
mock_scraper = MockWebScraper()
tools_data = mock_scraper.scrape_ai_tools()
```

### 2. 测试脚本

提供了独立的测试脚本（`test_mock_mode.py`）来验证核心功能：

```bash
python test_mock_mode.py
```

### 3. GitHub Actions配置

在`.github/workflows/`中添加以下环境变量：

```yaml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  GOOGLE_SHEETS_ID: ${{ secrets.GOOGLE_SHEETS_ID }}
  # 可选：如果没有外部依赖，系统会使用模拟数据
```

## 🚀 运行模式

### 完整模式（推荐在本地运行）
```bash
python main.py
```

### 测试模式（适合CI/CD）
```bash
python test_mock_mode.py
```

## 📊 模拟数据内容

模拟数据包含以下AI工具：

- ChatGPT-4
- Claude-3
- Midjourney V6
- Runway ML
- Perplexity AI
- Sora
- Gemini Ultra
- Stable Diffusion XL
- LangChain
- AutoGPT
- Copilot X
- Whisper Large

## 🔍 故障排除

### 1. 模块导入错误
确保所有模块都在正确的路径下：
```
src/
├── mock_web_scraper.py
├── openai_analyzer.py
├── data_processor.py
└── ...
```

### 2. 依赖版本问题
确保使用正确的库版本：
```bash
pip install -r requirements.txt
```

### 3. 环境变量配置
检查必要的环境变量：
```bash
# 必需
OPENAI_API_KEY=your_api_key_here

# 可选（如果要使用Google Sheets）
GOOGLE_SHEETS_ID=your_sheet_id_here
```

## 📈 运行结果

系统会生成以下输出：

- **processed_words.json**：处理后的词汇数据
- **ai_words_export.csv**：导出的CSV文件
- **调试信息**：详细的运行日志

## 🎯 GitHub Actions示例

```yaml
name: AI Words Mining
on:
  schedule:
    - cron: '0 0 * * *'  # 每天运行
  workflow_dispatch:

jobs:
  mine-words:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run AI Words Mining
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        GOOGLE_SHEETS_ID: ${{ secrets.GOOGLE_SHEETS_ID }}
      run: |
        python main.py
```

## 📚 相关文档

- [README.md](./README.md) - 项目总体介绍
- [config.py](./config.py) - 配置说明
- [requirements.txt](./requirements.txt) - 依赖列表 