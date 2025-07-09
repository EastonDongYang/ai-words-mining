#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from advanced_web_scraper import AdvancedWebScraper
import json

def test_advanced_scraper():
    """测试改进的爬虫功能"""
    print("🧪 测试改进的AI工具爬虫...")
    print("=" * 60)
    
    # 创建爬虫实例
    scraper = AdvancedWebScraper()
    
    # 测试URL
    test_url = "https://theresanaiforthat.com/trending/week/top-50/?pos=1"
    
    try:
        # 爬取数据
        print(f"🎯 目标URL: {test_url}")
        tools = scraper.scrape_ai_tools(test_url)
        
        # 显示结果
        print("\n" + "=" * 60)
        print("📊 爬取结果统计:")
        print(f"✅ 成功获取 {len(tools)} 个AI工具")
        
        if tools:
            print("\n🏆 前5个工具预览:")
            for i, tool in enumerate(tools[:5]):
                print(f"\n{i+1}. {tool.get('name', 'Unknown')}")
                print(f"   描述: {tool.get('description', 'No description')[:100]}...")
                print(f"   分类: {tool.get('category', 'Unknown')}")
                print(f"   链接: {tool.get('link', 'No link')}")
            
            # 保存结果到文件
            output_file = "scraped_tools_advanced.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(tools, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 结果已保存到: {output_file}")
            
            # 分析结果
            print("\n📈 数据分析:")
            categories = {}
            for tool in tools:
                cat = tool.get('category', 'Unknown')
                categories[cat] = categories.get(cat, 0) + 1
            
            print(f"📊 分类统计:")
            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                print(f"   {cat}: {count} 个工具")
            
            # 检查数据质量
            quality_metrics = {
                'has_name': sum(1 for tool in tools if tool.get('name') and len(tool.get('name', '').strip()) > 2),
                'has_description': sum(1 for tool in tools if tool.get('description') and len(tool.get('description', '').strip()) > 10),
                'has_link': sum(1 for tool in tools if tool.get('link') and 'http' in tool.get('link', '')),
                'has_category': sum(1 for tool in tools if tool.get('category') and tool.get('category') != 'Unknown')
            }
            
            print(f"\n📊 数据质量分析:")
            print(f"   有效名称: {quality_metrics['has_name']}/{len(tools)} ({quality_metrics['has_name']/len(tools)*100:.1f}%)")
            print(f"   有效描述: {quality_metrics['has_description']}/{len(tools)} ({quality_metrics['has_description']/len(tools)*100:.1f}%)")
            print(f"   有效链接: {quality_metrics['has_link']}/{len(tools)} ({quality_metrics['has_link']/len(tools)*100:.1f}%)")
            print(f"   有效分类: {quality_metrics['has_category']}/{len(tools)} ({quality_metrics['has_category']/len(tools)*100:.1f}%)")
            
            return True
            
        else:
            print("❌ 没有获取到任何工具数据")
            print("💡 可能原因:")
            print("   - 网站结构发生变化")
            print("   - 网站有反爬虫保护")
            print("   - 网络连接问题")
            print("   - 需要调整选择器策略")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_advanced_scraper()
    print("\n" + "=" * 60)
    if success:
        print("🎉 改进的爬虫测试成功！")
    else:
        print("❌ 改进的爬虫测试失败")
        print("💡 请检查网络连接和依赖安装")
    print("=" * 60) 