#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.multi_site_scraper import MultiSiteScraper

print("🧪 快速测试多网站爬虫...")
scraper = MultiSiteScraper()
tools = scraper.scrape_all_sites()

print(f"📊 获取到 {len(tools)} 个工具")
for i, tool in enumerate(tools[:5], 1):
    print(f"{i}. {tool.get('name', 'Unknown')} (来源: {tool.get('source', 'unknown')})")

if tools:
    print("✅ 多网站爬虫基本功能正常")
else:
    print("⚠️ 没有获取到数据，但系统没有崩溃") 