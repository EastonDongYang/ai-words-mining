#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import json
import random
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import config

class AdvancedWebScraper:
    """
    使用高级技巧的Web爬虫，专门针对theresanaiforthat.com
    结合了反反爬虫技术和多种备选策略
    """
    
    def __init__(self):
        self.config = config.Config()
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """设置请求会话的高级配置"""
        # 使用更真实的User-Agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        
        self.session.headers.update(headers)
        
    def get_chrome_options(self, headless=True):
        """获取Chrome浏览器的高级选项配置"""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless=new")
            
        # 反反爬虫技术
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        
        # 实验性选项
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # 设置随机User-Agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
        
        return chrome_options
    
    def scrape_with_selenium(self, url, max_retries=3):
        """使用Selenium爬取网页"""
        for attempt in range(max_retries):
            try:
                print(f"🔄 使用Selenium爬取 (尝试 {attempt + 1}/{max_retries}): {url}")
                
                # 设置Chrome选项
                chrome_options = self.get_chrome_options(headless=True)
                
                # 尝试使用webdriver-manager自动管理ChromeDriver
                try:
                    service = Service(ChromeDriverManager().install())
                except Exception as e:
                    print(f"⚠️ webdriver-manager失败: {e}")
                    # 回退到手动路径
                    chromedriver_paths = [
                        os.path.join(os.getcwd(), "chromedriver.exe"),
                        os.path.join(os.getcwd(), "drivers", "chromedriver.exe"),
                        r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"
                    ]
                    
                    chromedriver_path = None
                    for path in chromedriver_paths:
                        if os.path.exists(path):
                            chromedriver_path = path
                            break
                    
                    if not chromedriver_path:
                        raise Exception("找不到ChromeDriver")
                    
                    service = Service(executable_path=chromedriver_path)
                
                # 创建WebDriver
                driver = webdriver.Chrome(service=service, options=chrome_options)
                
                try:
                    # 执行反检测脚本
                    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                    
                    # 访问网页
                    driver.get(url)
                    print("✅ 页面加载成功")
                    
                    # 随机等待
                    time.sleep(random.uniform(3, 7))
                    
                    # 模拟人类行为 - 滚动页面
                    self.simulate_human_behavior(driver)
                    
                    # 等待页面内容加载
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    
                    # 获取页面源码
                    html_content = driver.page_source
                    
                    # 尝试提取AI工具数据
                    tools_data = self.extract_ai_tools_selenium(driver)
                    
                    return {
                        'html': html_content,
                        'tools': tools_data,
                        'method': 'selenium',
                        'success': True
                    }
                    
                finally:
                    driver.quit()
                    
            except Exception as e:
                print(f"❌ Selenium爬取失败 (尝试 {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    wait_time = random.uniform(5, 15)
                    print(f"⏳ 等待 {wait_time:.1f} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print("❌ Selenium爬取最终失败")
                    
        return None
    
    def simulate_human_behavior(self, driver):
        """模拟人类浏览行为"""
        try:
            # 随机滚动
            scroll_actions = [
                "window.scrollTo(0, document.body.scrollHeight/4);",
                "window.scrollTo(0, document.body.scrollHeight/2);",
                "window.scrollTo(0, document.body.scrollHeight/3);",
                "window.scrollTo(0, document.body.scrollHeight);",
                "window.scrollTo(0, 0);"
            ]
            
            for action in random.sample(scroll_actions, k=min(3, len(scroll_actions))):
                driver.execute_script(action)
                time.sleep(random.uniform(1, 3))
                
            # 最后滚动到底部
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            print(f"⚠️ 模拟人类行为时出错: {e}")
    
    def extract_ai_tools_selenium(self, driver):
        """使用Selenium提取AI工具数据"""
        tools = []
        
        try:
            # 针对theresanaiforthat.com的多种选择器策略
            selectors = [
                "div.tool-card",
                "div[class*='tool']",
                "div[class*='card']",
                "div[class*='item']",
                "article",
                ".tool-item",
                ".ai-tool",
                "[data-tool]",
                "div.grid > div",
                "div.list-item"
            ]
            
            elements = []
            for selector in selectors:
                try:
                    found_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if found_elements:
                        print(f"✅ 找到 {len(found_elements)} 个元素使用选择器: {selector}")
                        elements = found_elements
                        break
                except Exception as e:
                    print(f"⚠️ 选择器 {selector} 失败: {e}")
                    continue
            
            if not elements:
                print("❌ 未找到任何工具元素")
                return []
            
            # 提取工具信息
            for i, element in enumerate(elements[:50]):  # 限制最多处理50个
                try:
                    tool_data = self.extract_tool_info_selenium(element, i + 1)
                    if tool_data:
                        tools.append(tool_data)
                        print(f"✅ 提取工具 {i + 1}: {tool_data.get('name', 'Unknown')}")
                except Exception as e:
                    print(f"⚠️ 提取工具 {i + 1} 失败: {e}")
                    continue
            
            print(f"📊 总共提取了 {len(tools)} 个AI工具")
            return tools
            
        except Exception as e:
            print(f"❌ 提取AI工具数据失败: {e}")
            return []
    
    def extract_tool_info_selenium(self, element, index):
        """从单个元素中提取工具信息"""
        try:
            # 提取工具名称
            name_selectors = [
                "h1", "h2", "h3", "h4", "h5", "h6",
                ".title", ".name", ".tool-name", ".tool-title",
                "[class*='title']", "[class*='name']",
                "a[href*='tool']", "a[href*='app']"
            ]
            
            name = ""
            for selector in name_selectors:
                try:
                    name_element = element.find_element(By.CSS_SELECTOR, selector)
                    if name_element and name_element.text.strip():
                        name = name_element.text.strip()
                        break
                except:
                    continue
            
            # 提取描述
            description_selectors = [
                ".description", ".desc", ".summary", ".info",
                "p", ".content", ".text", "[class*='desc']",
                "[class*='summary']", "[class*='info']"
            ]
            
            description = ""
            for selector in description_selectors:
                try:
                    desc_element = element.find_element(By.CSS_SELECTOR, selector)
                    if desc_element and desc_element.text.strip():
                        description = desc_element.text.strip()
                        break
                except:
                    continue
            
            # 提取链接
            link_selectors = [
                "a[href*='http']", "a[href*='www']", "a[href*='tool']",
                "a[href*='app']", "a", "[href]"
            ]
            
            link = ""
            for selector in link_selectors:
                try:
                    link_element = element.find_element(By.CSS_SELECTOR, selector)
                    href = link_element.get_attribute("href")
                    if href and ("http" in href or "www" in href):
                        link = href
                        break
                except:
                    continue
            
            # 提取分类/标签
            category_selectors = [
                ".category", ".tag", ".type", ".genre",
                "[class*='category']", "[class*='tag']", "[class*='type']",
                ".badge", ".label", "span"
            ]
            
            category = ""
            for selector in category_selectors:
                try:
                    cat_element = element.find_element(By.CSS_SELECTOR, selector)
                    if cat_element and cat_element.text.strip():
                        category = cat_element.text.strip()
                        break
                except:
                    continue
            
            # 只返回有效的工具数据
            if name and len(name) > 2:
                return {
                    'name': name,
                    'description': description,
                    'link': link,
                    'category': category,
                    'source': 'theresanaiforthat.com',
                    'scraped_at': datetime.now().isoformat(),
                    'index': index
                }
            
            return None
            
        except Exception as e:
            print(f"⚠️ 提取工具信息失败: {e}")
            return None
    
    def scrape_with_requests(self, url, max_retries=3):
        """使用requests爬取网页的高级版本"""
        for attempt in range(max_retries):
            try:
                print(f"🔄 使用requests爬取 (尝试 {attempt + 1}/{max_retries}): {url}")
                
                # 随机等待
                time.sleep(random.uniform(2, 5))
                
                # 发送请求
                response = self.session.get(url, timeout=30)
                
                if response.status_code == 200:
                    print("✅ 成功获取页面内容")
                    
                    # 解析HTML
                    soup = BeautifulSoup(response.text, 'html.parser')
                    tools_data = self.extract_ai_tools_requests(soup)
                    
                    return {
                        'html': response.text,
                        'tools': tools_data,
                        'method': 'requests',
                        'success': True
                    }
                    
                else:
                    print(f"❌ HTTP错误: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Requests爬取失败 (尝试 {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    wait_time = random.uniform(3, 10)
                    print(f"⏳ 等待 {wait_time:.1f} 秒后重试...")
                    time.sleep(wait_time)
                    
                    # 更换User-Agent
                    user_agents = [
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
                    ]
                    self.session.headers.update({'User-Agent': random.choice(user_agents)})
                    
        return None
    
    def extract_ai_tools_requests(self, soup):
        """使用BeautifulSoup提取AI工具数据"""
        tools = []
        
        try:
            # 针对theresanaiforthat.com的多种选择器策略
            selectors = [
                "div.tool-card",
                "div[class*='tool']",
                "div[class*='card']",
                "div[class*='item']",
                "article",
                ".tool-item",
                ".ai-tool",
                "[data-tool]"
            ]
            
            elements = []
            for selector in selectors:
                try:
                    found_elements = soup.select(selector)
                    if found_elements:
                        print(f"✅ 找到 {len(found_elements)} 个元素使用选择器: {selector}")
                        elements = found_elements
                        break
                except Exception as e:
                    print(f"⚠️ 选择器 {selector} 失败: {e}")
                    continue
            
            if not elements:
                print("❌ 未找到任何工具元素")
                return []
            
            # 提取工具信息
            for i, element in enumerate(elements[:50]):  # 限制最多处理50个
                try:
                    tool_data = self.extract_tool_info_requests(element, i + 1)
                    if tool_data:
                        tools.append(tool_data)
                        print(f"✅ 提取工具 {i + 1}: {tool_data.get('name', 'Unknown')}")
                except Exception as e:
                    print(f"⚠️ 提取工具 {i + 1} 失败: {e}")
                    continue
            
            print(f"📊 总共提取了 {len(tools)} 个AI工具")
            return tools
            
        except Exception as e:
            print(f"❌ 提取AI工具数据失败: {e}")
            return []
    
    def extract_tool_info_requests(self, element, index):
        """从BeautifulSoup元素中提取工具信息"""
        try:
            # 提取工具名称
            name_selectors = [
                "h1", "h2", "h3", "h4", "h5", "h6",
                ".title", ".name", ".tool-name", ".tool-title",
                "[class*='title']", "[class*='name']"
            ]
            
            name = ""
            for selector in name_selectors:
                try:
                    name_element = element.select_one(selector)
                    if name_element and name_element.get_text().strip():
                        name = name_element.get_text().strip()
                        break
                except:
                    continue
            
            # 提取描述
            description_selectors = [
                ".description", ".desc", ".summary", ".info",
                "p", ".content", ".text"
            ]
            
            description = ""
            for selector in description_selectors:
                try:
                    desc_element = element.select_one(selector)
                    if desc_element and desc_element.get_text().strip():
                        description = desc_element.get_text().strip()
                        break
                except:
                    continue
            
            # 提取链接
            link = ""
            try:
                link_element = element.select_one("a[href]")
                if link_element:
                    link = link_element.get("href", "")
            except:
                pass
            
            # 提取分类
            category = ""
            try:
                category_element = element.select_one(".category, .tag, .type, .badge")
                if category_element:
                    category = category_element.get_text().strip()
            except:
                pass
            
            # 只返回有效的工具数据
            if name and len(name) > 2:
                return {
                    'name': name,
                    'description': description,
                    'link': link,
                    'category': category,
                    'source': 'theresanaiforthat.com',
                    'scraped_at': datetime.now().isoformat(),
                    'index': index
                }
            
            return None
            
        except Exception as e:
            print(f"⚠️ 提取工具信息失败: {e}")
            return None
    
    def scrape_ai_tools(self, url=None):
        """主要的爬取方法，结合多种策略"""
        if not url:
            url = self.config.TARGET_URL
        
        print(f"🚀 开始爬取AI工具: {url}")
        
        # 策略1: 先尝试Selenium
        result = self.scrape_with_selenium(url)
        if result and result['success'] and result['tools']:
            print(f"✅ Selenium爬取成功，获得 {len(result['tools'])} 个工具")
            return result['tools']
        
        # 策略2: 如果Selenium失败，尝试requests
        print("🔄 Selenium失败，尝试requests方法...")
        result = self.scrape_with_requests(url)
        if result and result['success'] and result['tools']:
            print(f"✅ Requests爬取成功，获得 {len(result['tools'])} 个工具")
            return result['tools']
        
        # 策略3: 如果都失败，返回空列表
        print("❌ 所有爬取方法都失败")
        return [] 