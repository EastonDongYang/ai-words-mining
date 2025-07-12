#!/usr/bin/env python3
"""
简化的爬虫测试 - 不使用Selenium
Simple Scraping Test - Without Selenium
"""

import sys
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import Config

def test_basic_requests():
    """测试基本的HTTP请求功能"""
    print("🧪 测试基本HTTP请求功能...")
    
    try:
        # 测试简单的HTTP请求
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # 测试一个简单的网站
        test_url = "https://httpbin.org/json"
        response = session.get(test_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ HTTP请求功能正常")
            return True
        else:
            print(f"❌ HTTP请求失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ HTTP请求测试失败: {e}")
        return False

def test_html_parsing():
    """测试HTML解析功能"""
    print("🧪 测试HTML解析功能...")
    
    try:
        # 创建测试HTML
        test_html = """
        <html>
        <head><title>Test</title></head>
        <body>
            <div class="tool-card">
                <h3 class="name">Test AI Tool</h3>
                <p class="description">This is a test AI tool description</p>
                <span class="tag">AI</span>
                <span class="tag">Test</span>
            </div>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(test_html, 'html.parser')
        
        # 测试提取功能
        name = soup.find('h3', class_='name').get_text(strip=True)
        description = soup.find('p', class_='description').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in soup.find_all('span', class_='tag')]
        
        if name == "Test AI Tool" and "test AI tool" in description.lower() and len(tags) == 2:
            print("✅ HTML解析功能正常")
            return True
        else:
            print("❌ HTML解析功能异常")
            return False
            
    except Exception as e:
        print(f"❌ HTML解析测试失败: {e}")
        return False

def test_betalist_scraping():
    """测试BetaList网站爬取（使用requests）"""
    print("🧪 测试BetaList网站爬取...")
    
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
        })
        
        url = "https://betalist.com/"
        print(f"正在访问: {url}")
        
        response = session.get(url, timeout=30)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 查找可能的产品元素
            possible_selectors = [
                'div[class*="startup"]',
                'div[class*="product"]', 
                'article',
                'div[class*="item"]',
                'div[class*="card"]'
            ]
            
            found_elements = []
            for selector in possible_selectors:
                elements = soup.select(selector)
                if elements:
                    found_elements.extend(elements)
                    print(f"找到 {len(elements)} 个元素使用选择器: {selector}")
            
            if found_elements:
                print(f"✅ 总共找到 {len(found_elements)} 个可能的产品元素")
                
                # 尝试提取前几个元素的信息
                extracted = 0
                for element in found_elements[:10]:
                    # 尝试提取标题
                    title_tags = element.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                    for title_tag in title_tags:
                        title_text = title_tag.get_text(strip=True)
                        if title_text and len(title_text) > 3 and len(title_text) < 100:
                            print(f"  - 发现产品: {title_text}")
                            extracted += 1
                            break
                
                if extracted > 0:
                    print(f"✅ 成功提取 {extracted} 个产品信息")
                    return True
                else:
                    print("⚠️ 找到了元素但未能提取产品信息")
                    return False
            else:
                print("⚠️ 未找到产品元素")
                return False
        else:
            print(f"❌ 网站访问失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ BetaList爬取测试失败: {e}")
        return False

def test_config_loading():
    """测试配置加载"""
    print("🧪 测试配置加载...")
    
    try:
        config = Config()
        
        print(f"目标网站数量: {len(config.TARGET_URLS)}")
        print(f"多网站爬虫启用: {config.ENABLE_MULTI_SITE}")
        print(f"最大总数量: {config.MAX_TOTAL_ITEMS}")
        
        if len(config.TARGET_URLS) >= 6 and config.ENABLE_MULTI_SITE:
            print("✅ 配置加载正常")
            return True
        else:
            print("❌ 配置加载异常")
            return False
            
    except Exception as e:
        print(f"❌ 配置加载测试失败: {e}")
        return False

def test_openai_analyzer():
    """测试OpenAI分析器（不实际调用API）"""
    print("🧪 测试OpenAI分析器配置...")
    
    try:
        # 只测试导入和初始化，不实际调用API
        from src.openai_analyzer import OpenAIAnalyzer
        
        analyzer = OpenAIAnalyzer()
        
        if hasattr(analyzer, 'config') and hasattr(analyzer, 'client'):
            print("✅ OpenAI分析器配置正常")
            return True
        else:
            print("❌ OpenAI分析器配置异常")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI分析器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🎯 简化爬虫功能测试")
    print("=" * 50)
    
    tests = [
        ("配置加载", test_config_loading),
        ("基本HTTP请求", test_basic_requests),
        ("HTML解析功能", test_html_parsing),
        ("OpenAI分析器", test_openai_analyzer),
        ("BetaList爬取", test_betalist_scraping),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} 测试出现异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有基础功能测试通过！")
        print("💡 Chrome WebDriver问题需要单独解决")
    elif passed >= total // 2:
        print("⚠️ 部分功能正常，需要解决一些问题")
    else:
        print("❌ 多数功能异常，需要检查环境配置")
    
    return passed >= total // 2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 