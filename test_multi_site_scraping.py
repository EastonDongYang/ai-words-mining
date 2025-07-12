#!/usr/bin/env python3
"""
测试多网站爬虫功能
Test Multi-Site Scraping Functionality
"""

import sys
import os
from datetime import datetime

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import Config
from src.multi_site_scraper import MultiSiteScraper

def test_multi_site_scraping():
    """测试多网站爬虫功能"""
    print("🧪 开始测试多网站爬虫功能...")
    print("=" * 60)
    
    try:
        # 创建配置和爬虫实例
        config = Config()
        scraper = MultiSiteScraper()
        
        # 打印配置信息
        print("📋 配置信息：")
        print(f"  多网站爬虫启用: {config.ENABLE_MULTI_SITE}")
        print(f"  目标网站数量: {len(config.TARGET_URLS)}")
        print(f"  最大总数量: {config.MAX_TOTAL_ITEMS}")
        print(f"  调试模式: {config.DEBUG_MODE}")
        print()
        
        # 打印要爬取的网站
        print("🌐 目标网站列表：")
        for i, url in enumerate(config.TARGET_URLS, 1):
            print(f"  {i}. {url}")
        print()
        
        # 打印启用的网站配置
        print("⚙️ 网站配置：")
        for site in config.get_enabled_sites():
            site_config = config.get_site_config(site)
            print(f"  {site}:")
            print(f"    - 启用: {site_config.get('enabled', True)}")
            print(f"    - 最大数量: {site_config.get('max_items', 30)}")
            print(f"    - 延迟: {site_config.get('delay', 2)}秒")
            print(f"    - 使用Selenium: {site_config.get('use_selenium', True)}")
        print()
        
        # 开始爬取测试
        print("🚀 开始爬取测试...")
        start_time = datetime.now()
        
        # 执行爬取
        all_tools = scraper.scrape_all_sites()
        
        end_time = datetime.now()
        execution_time = end_time - start_time
        
        # 分析结果
        print(f"⏱️ 爬取耗时: {execution_time}")
        print(f"📊 总共获取: {len(all_tools)} 个工具/产品")
        
        if all_tools:
            # 按来源分组统计
            source_stats = {}
            for tool in all_tools:
                source = tool.get('source', 'unknown')
                source_stats[source] = source_stats.get(source, 0) + 1
            
            print("\n📈 来源统计:")
            for source, count in sorted(source_stats.items()):
                print(f"  - {source}: {count} 个")
            
            # 显示前10个工具示例
            print("\n🔍 前10个工具示例:")
            for i, tool in enumerate(all_tools[:10], 1):
                print(f"  {i}. {tool.get('name', 'Unknown')}")
                print(f"     来源: {tool.get('source', 'unknown')}")
                print(f"     描述: {tool.get('description', 'No description')[:100]}...")
                print(f"     类别: {', '.join(tool.get('categories', []))}")
                print()
            
            # 保存结果
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"test_multi_site_results_{timestamp}.json"
            scraper.save_results(all_tools, filename)
            
            print(f"✅ 测试完成！结果已保存到: {filename}")
            return True
        else:
            print("❌ 没有获取到任何数据")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_single_site():
    """测试单个网站爬取"""
    print("\n🧪 测试单个网站爬取...")
    
    try:
        config = Config()
        scraper = MultiSiteScraper()
        
        # 测试第一个网站
        test_url = config.TARGET_URLS[0]
        print(f"🔗 测试网站: {test_url}")
        
        from urllib.parse import urlparse
        site_domain = urlparse(test_url).netloc
        site_config = config.get_site_config(site_domain)
        
        tools = scraper.scrape_site(test_url, site_config)
        
        if tools:
            print(f"✅ 成功获取 {len(tools)} 个工具")
            print("📝 示例工具:")
            for i, tool in enumerate(tools[:3], 1):
                print(f"  {i}. {tool.get('name', 'Unknown')}")
                print(f"     描述: {tool.get('description', 'No description')[:80]}...")
        else:
            print("⚠️ 没有获取到工具")
            
    except Exception as e:
        print(f"❌ 单网站测试失败: {e}")

def main():
    """主测试函数"""
    print("🎯 多网站爬虫测试套件")
    print("=" * 60)
    
    # 测试多网站爬取
    success = test_multi_site_scraping()
    
    # 测试单网站爬取
    test_single_site()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 所有测试完成！")
        print("💡 提示: 查看生成的JSON文件获取详细结果")
    else:
        print("⚠️ 测试过程中遇到问题，请检查网络连接和配置")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 