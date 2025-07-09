#!/usr/bin/env python3
"""
测试网页爬取功能
"""

import sys
import os
import json

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import Config
from src.web_scraper import AIToolsScraper

def test_scraper():
    """测试爬取功能"""
    print("🧪 测试网页爬取功能...")
    
    try:
        # 创建爬虫实例
        scraper = AIToolsScraper()
        
        # 测试网页爬取
        print(f"🕷️ 开始爬取: {scraper.config.TARGET_URL}")
        
        # 使用fallback方法先测试
        tools_data = scraper.scrape_with_requests(scraper.config.TARGET_URL)
        
        if tools_data:
            print(f"✅ 成功爬取到 {len(tools_data)} 个工具")
            print("\n📋 示例数据:")
            for i, tool in enumerate(tools_data[:3]):  # 显示前3个
                print(f"{i+1}. {tool['name']}")
                print(f"   描述: {tool['description'][:100]}...")
                print(f"   分类: {tool.get('categories', [])}")
                print()
            
            # 保存到文件
            with open('test_scraped_data.json', 'w', encoding='utf-8') as f:
                json.dump(tools_data, f, indent=2, ensure_ascii=False)
            
            print(f"📄 数据已保存到 test_scraped_data.json")
            return True
            
        else:
            print("❌ 没有爬取到数据")
            return False
            
    except Exception as e:
        print(f"❌ 爬取测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_scraper()
    sys.exit(0 if success else 1) 