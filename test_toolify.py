#!/usr/bin/env python3
"""
专门测试Toolify.ai网站爬取
"""
import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def setup_driver():
    """Setup Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        driver_path = ChromeDriverManager().install()
        
        # Fix path issue
        if driver_path.endswith('THIRD_PARTY_NOTICES.chromedriver'):
            driver_dir = os.path.dirname(driver_path)
            driver_path = os.path.join(driver_dir, 'chromedriver.exe')
        
        print(f"Using driver: {driver_path}")
        service = webdriver.chrome.service.Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
        
    except Exception as e:
        print(f"Driver setup failed: {e}")
        raise

def test_toolify():
    """测试Toolify.ai网站"""
    url = "https://www.toolify.ai/new"
    driver = None
    
    try:
        print(f"🔗 正在访问: {url}")
        driver = setup_driver()
        driver.get(url)
        
        print("⏳ 等待页面加载...")
        time.sleep(5)
        
        # 获取页面标题
        title = driver.title
        print(f"📄 页面标题: {title}")
        
        # 滚动页面加载更多内容
        print("📜 滚动页面...")
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # 获取页面源码并用BeautifulSoup解析
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        print(f"📊 页面内容长度: {len(html)} 字符")
        
        # 尝试各种可能的选择器
        selectors_to_try = [
            '.tool-card',
            '[data-testid="tool-card"]',
            '.ai-tool-card',
            '.grid-item',
            '.tool-item',
            '.tool',
            'article',
            '.card',
            'div[class*="tool"]',
            'div[class*="card"]',
            'div[class*="item"]',
            '.product',
            '.list-item',
            '[role="article"]'
        ]
        
        found_elements = []
        for selector in selectors_to_try:
            try:
                if selector.startswith('.') or selector.startswith('['):
                    elements = soup.select(selector)
                else:
                    elements = soup.find_all(selector)
                
                if elements:
                    print(f"✅ 选择器 '{selector}' 找到 {len(elements)} 个元素")
                    found_elements.extend(elements)
                else:
                    print(f"❌ 选择器 '{selector}' 没有找到元素")
            except Exception as e:
                print(f"⚠️ 选择器 '{selector}' 错误: {e}")
        
        if found_elements:
            print(f"\n📋 总共找到 {len(found_elements)} 个可能的工具元素")
            
            # 尝试提取前几个元素的信息
            for i, element in enumerate(found_elements[:5], 1):
                print(f"\n🔍 分析元素 {i}:")
                
                # 查找标题
                title_found = False
                for title_tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    titles = element.find_all(title_tag)
                    for title_elem in titles:
                        text = title_elem.get_text(strip=True)
                        if text and len(text) > 2 and len(text) < 100:
                            print(f"  📝 标题 ({title_tag}): {text}")
                            title_found = True
                            break
                    if title_found:
                        break
                
                # 查找描述
                for desc_tag in ['p', 'div', 'span']:
                    descs = element.find_all(desc_tag)
                    for desc_elem in descs[:2]:  # 只看前2个
                        text = desc_elem.get_text(strip=True)
                        if text and len(text) > 10 and len(text) < 200:
                            print(f"  📄 描述 ({desc_tag}): {text[:80]}...")
                            break
                
                # 查找链接
                links = element.find_all('a')
                for link in links[:2]:
                    href = link.get('href', '')
                    text = link.get_text(strip=True)
                    if href and text:
                        print(f"  🔗 链接: {text} -> {href[:50]}")
        else:
            print("❌ 没有找到任何工具元素")
            
            # 输出页面的基本结构
            print("\n📋 页面基本结构:")
            body = soup.find('body')
            if body:
                # 查找所有div元素
                divs = body.find_all('div', limit=20)
                print(f"找到 {len(divs)} 个div元素")
                
                for i, div in enumerate(divs[:10], 1):
                    class_attr = div.get('class', [])
                    id_attr = div.get('id', '')
                    if class_attr or id_attr:
                        print(f"  div {i}: class={class_attr}, id={id_attr}")
        
        return len(found_elements) > 0
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    print("🧪 专门测试Toolify.ai爬取")
    print("=" * 50)
    success = test_toolify()
    print("=" * 50)
    if success:
        print("✅ 找到了一些元素，需要优化选择器")
    else:
        print("❌ 没有找到有用的元素，需要分析页面结构") 