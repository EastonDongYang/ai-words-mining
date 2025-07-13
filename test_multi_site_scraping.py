#!/usr/bin/env python3
"""
测试多网站爬取功能
"""

import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import Config
from src.multi_site_scraper import MultiSiteScraper

def test_individual_sites():
    """测试单个网站的爬取效果"""
    print("🧪 测试单个网站爬取功能...")
    
    config = Config()
    scraper = MultiSiteScraper()
    
    # 显示配置信息
    print(f"\n📋 配置信息:")
    print(f"  - 多网站爬取: {config.ENABLE_MULTI_SITE}")
    print(f"  - 总数限制: {config.MAX_TOTAL_ITEMS}")
    print(f"  - 目标网站数: {len(config.TARGET_URLS)}")
    print(f"  - 启用的网站: {len(config.get_enabled_sites())}")
    
    results = {}
    
    for url in config.TARGET_URLS:
        try:
            from urllib.parse import urlparse
            site_domain = urlparse(url).netloc
            site_config = config.get_site_config(site_domain)
            
            print(f"\n🕷️ 测试 {site_domain}...")
            print(f"  - URL: {url}")
            print(f"  - 启用状态: {'✅' if site_config.get('enabled', True) else '❌'}")
            print(f"  - 最大项目数: {site_config.get('max_items', 30)}")
            print(f"  - 使用Selenium: {'✅' if site_config.get('use_selenium', True) else '❌'}")
            
            if not site_config.get('enabled', True):
                print(f"  ⚠️ 网站已禁用，跳过")
                results[site_domain] = {'status': 'disabled', 'count': 0}
                continue
            
            # 尝试爬取
            start_time = datetime.now()
            tools = scraper.scrape_site(url, site_config)
            end_time = datetime.now()
            
            execution_time = (end_time - start_time).total_seconds()
            
            if tools:
                print(f"  ✅ 成功爬取 {len(tools)} 个项目 (耗时: {execution_time:.2f}秒)")
                results[site_domain] = {
                    'status': 'success', 
                    'count': len(tools),
                    'execution_time': execution_time,
                    'sample_items': tools[:3]  # 保存前3个样本
                }
            else:
                print(f"  ❌ 未找到任何项目 (耗时: {execution_time:.2f}秒)")
                results[site_domain] = {
                    'status': 'no_data', 
                    'count': 0,
                    'execution_time': execution_time
                }
                
        except Exception as e:
            print(f"  ❌ 爬取失败: {e}")
            results[site_domain] = {'status': 'error', 'count': 0, 'error': str(e)}
    
    return results

def test_multi_site_scraping():
    """测试多网站综合爬取"""
    print("\n🌐 测试多网站综合爬取...")
    
    scraper = MultiSiteScraper()
    
    try:
        start_time = datetime.now()
        all_tools = scraper.scrape_all_sites()
        end_time = datetime.now()
        
        execution_time = (end_time - start_time).total_seconds()
        
        print(f"\n📊 综合爬取结果:")
        print(f"  - 总项目数: {len(all_tools)}")
        print(f"  - 总耗时: {execution_time:.2f}秒")
        print(f"  - 平均每项耗时: {execution_time/len(all_tools):.2f}秒" if all_tools else "  - 无数据")
        
        # 按来源统计
        source_stats = {}
        for tool in all_tools:
            source = tool.get('source', 'unknown')
            source_stats[source] = source_stats.get(source, 0) + 1
        
        print(f"\n📈 按来源统计:")
        for source, count in sorted(source_stats.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {source}: {count} 个项目")
        
        return all_tools
        
    except Exception as e:
        print(f"❌ 多网站爬取失败: {e}")
        return []

def analyze_results(individual_results, multi_site_results):
    """分析爬取结果"""
    print("\n📋 结果分析:")
    
    # 统计各网站状态
    enabled_count = sum(1 for r in individual_results.values() if r['status'] != 'disabled')
    success_count = sum(1 for r in individual_results.values() if r['status'] == 'success')
    failed_count = sum(1 for r in individual_results.values() if r['status'] in ['error', 'no_data'])
    
    print(f"  - 启用的网站: {enabled_count}")
    print(f"  - 成功爬取: {success_count}")
    print(f"  - 失败/无数据: {failed_count}")
    print(f"  - 综合结果: {len(multi_site_results)} 个项目")
    
    # 识别问题网站
    problem_sites = []
    for site, result in individual_results.items():
        if result['status'] in ['error', 'no_data']:
            problem_sites.append(site)
    
    if problem_sites:
        print(f"\n⚠️ 需要关注的网站:")
        for site in problem_sites:
            result = individual_results[site]
            print(f"  - {site}: {result['status']}")
            if 'error' in result:
                print(f"    错误信息: {result['error']}")

def main():
    """主函数"""
    print("🚀 开始多网站爬取测试...")
    print("="*60)
    
    try:
        # 测试单个网站
        individual_results = test_individual_sites()
        
        # 测试综合爬取
        multi_site_results = test_multi_site_scraping()
        
        # 分析结果
        analyze_results(individual_results, multi_site_results)
        
        print("\n✅ 测试完成!")
        print("\n💡 建议:")
        print("1. 检查失败的网站，可能需要更新爬虫逻辑")
        print("2. 如果数据量仍然不足，可以调整max_items配置")
        print("3. 考虑添加更多目标网站")
        print("4. 检查网络连接和Chrome WebDriver设置")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 