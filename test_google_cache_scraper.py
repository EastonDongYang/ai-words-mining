#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import requests
import json
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

class GoogleCacheScraper:
    """
    专门使用Google缓存的爬虫
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
    
    def setup_session(self):
        """设置会话"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(headers)
    
    def get_google_cache(self, url):
        """获取Google缓存内容"""
        cache_url = f"https://webcache.googleusercontent.com/search?q=cache:{url}"
        
        try:
            print(f"🔄 获取Google缓存: {url}")
            response = self.session.get(cache_url, timeout=30)
            
            if response.status_code == 200:
                print("✅ Google缓存获取成功")
                return response.text
            else:
                print(f"❌ Google缓存失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 获取Google缓存时出错: {e}")
            return None
    
    def extract_tools_from_cache(self, html_content, original_url):
        """从缓存的HTML中提取工具数据"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            tools = []
            
            print("🔍 开始从缓存内容中提取工具...")
            
            # 查找所有可能的工具链接
            all_links = soup.find_all('a', href=True)
            print(f"📋 找到 {len(all_links)} 个链接")
            
            for i, link in enumerate(all_links):
                try:
                    href = link.get('href', '')
                    text = link.get_text().strip()
                    
                    # 过滤可能的工具链接
                    if (text and len(text) > 3 and len(text) < 200 and
                        not any(skip in href.lower() for skip in ['#', 'javascript:', 'mailto:', 'tel:', 'cache:', 'webcache']) and
                        not any(skip in text.lower() for skip in ['click here', 'read more', 'learn more', 'sign up', 'login', 'register'])):
                        
                        # 获取父元素的更多信息
                        parent = link.parent
                        description = ""
                        
                        # 尝试获取描述
                        if parent:
                            # 查找相邻的描述文本
                            for sibling in parent.find_next_siblings():
                                if sibling.get_text().strip():
                                    description = sibling.get_text().strip()[:500]
                                    break
                            
                            # 如果没有找到，尝试父元素的文本
                            if not description:
                                parent_text = parent.get_text().strip()
                                if parent_text and len(parent_text) > len(text):
                                    description = parent_text[:500]
                        
                        # 尝试从URL推断分类
                        category = "Unknown"
                        if any(cat in href.lower() for cat in ['ai', 'artificial-intelligence']):
                            category = "AI"
                        elif any(cat in href.lower() for cat in ['tool', 'productivity']):
                            category = "Productivity"
                        elif any(cat in href.lower() for cat in ['design', 'creative']):
                            category = "Design"
                        elif any(cat in href.lower() for cat in ['business', 'marketing']):
                            category = "Business"
                        
                        tool_data = {
                            'name': text,
                            'description': description,
                            'link': href if href.startswith('http') else urljoin(original_url, href),
                            'category': category,
                            'source': 'theresanaiforthat.com (cached)',
                            'scraped_at': datetime.now().isoformat(),
                            'index': i + 1
                        }
                        
                        tools.append(tool_data)
                        
                        if len(tools) >= 50:  # 限制最多50个工具
                            break
                        
                except Exception as e:
                    continue
            
            # 去重
            unique_tools = []
            seen_names = set()
            for tool in tools:
                name = tool['name'].lower()
                if name not in seen_names and len(name) > 2:
                    seen_names.add(name)
                    unique_tools.append(tool)
            
            print(f"📊 提取了 {len(unique_tools)} 个去重后的工具")
            return unique_tools
            
        except Exception as e:
            print(f"❌ 从缓存提取工具失败: {e}")
            return []
    
    def scrape_from_cache(self, url):
        """从缓存爬取数据"""
        # 获取缓存内容
        cached_html = self.get_google_cache(url)
        
        if cached_html:
            # 提取工具数据
            tools = self.extract_tools_from_cache(cached_html, url)
            return tools
        else:
            return []

def test_google_cache_scraper():
    """测试Google缓存爬虫"""
    print("🚀 测试Google缓存爬虫...")
    print("=" * 60)
    
    # 创建爬虫实例
    scraper = GoogleCacheScraper()
    
    # 测试URL
    test_url = "https://theresanaiforthat.com/trending/week/top-50/?pos=1"
    
    try:
        # 爬取数据
        print(f"🎯 目标URL: {test_url}")
        tools = scraper.scrape_from_cache(test_url)
        
        # 显示结果
        print("\n" + "=" * 60)
        print("📊 爬取结果统计:")
        print(f"✅ 成功获取 {len(tools)} 个AI工具")
        
        if tools:
            print("\n🏆 前10个工具预览:")
            for i, tool in enumerate(tools[:10]):
                print(f"\n{i+1}. {tool.get('name', 'Unknown')}")
                print(f"   描述: {tool.get('description', 'No description')[:100]}...")
                print(f"   分类: {tool.get('category', 'Unknown')}")
                print(f"   链接: {tool.get('link', 'No link')}")
            
            # 保存结果到文件
            output_file = "scraped_tools_cache.json"
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
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_google_cache_scraper()
    print("\n" + "=" * 60)
    if success:
        print("🎉 Google缓存爬虫测试成功！")
        print("💡 可以作为主要爬虫的备选方案")
    else:
        print("❌ Google缓存爬虫测试失败")
        print("💡 请检查网络连接和缓存可用性")
    print("=" * 60) 