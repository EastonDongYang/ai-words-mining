#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from super_scraper import SuperScraper
import json

def test_super_scraper():
    """测试超级爬虫功能"""
    print("🚀 测试超级AI工具爬虫...")
    print("=" * 60)
    
    # 创建爬虫实例
    scraper = SuperScraper()
    
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
            print("\n🏆 前10个工具预览:")
            for i, tool in enumerate(tools[:10]):
                print(f"\n{i+1}. {tool.get('name', 'Unknown')}")
                print(f"   描述: {tool.get('description', 'No description')[:150]}...")
                print(f"   分类: {tool.get('category', 'Unknown')}")
                print(f"   链接: {tool.get('link', 'No link')}")
            
            # 保存结果到文件
            output_file = "scraped_tools_super.json"
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
            
            # 检查是否有重复数据
            names = [tool.get('name', '') for tool in tools]
            unique_names = set(names)
            duplicate_rate = (len(names) - len(unique_names)) / len(names) * 100 if names else 0
            print(f"   重复率: {duplicate_rate:.1f}%")
            
            return True
            
        else:
            print("❌ 没有获取到任何工具数据")
            print("💡 可能原因:")
            print("   - 网站结构发生变化")
            print("   - 网站有强力反爬虫保护")
            print("   - 网络连接问题")
            print("   - 需要调整选择器策略")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_super_scraper()
    print("\n" + "=" * 60)
    if success:
        print("🎉 超级爬虫测试成功！")
        print("💡 现在可以将这个超级爬虫集成到主系统中")
    else:
        print("❌ 超级爬虫测试失败")
        print("💡 请检查网络连接和目标网站状态")
    print("=" * 60) 