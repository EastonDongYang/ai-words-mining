#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import json
import random
import requests
from datetime import datetime
from urllib.parse import urljoin, urlparse
import config

class SuperScraper:
    """
    超级爬虫 - 使用多种技术绕过反爬虫机制
    """
    
    def __init__(self):
        self.config = config.Config()
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """设置高级会话配置"""
        # 轮换User-Agent池
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        ]
        
        # 随机选择User-Agent
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Sec-GPC': '1'
        }
        
        self.session.headers.update(headers)
        
        # 设置代理（如果需要）
        # self.session.proxies = {'http': 'http://proxy:port', 'https': 'https://proxy:port'}
    
    def get_with_retry(self, url, max_retries=5, backoff_factor=1.5):
        """
        带重试和退避策略的GET请求
        """
        for attempt in range(max_retries):
            try:
                print(f"🔄 请求尝试 {attempt + 1}/{max_retries}: {url}")
                
                # 随机等待
                time.sleep(random.uniform(2, 6))
                
                # 轮换User-Agent
                self.session.headers['User-Agent'] = random.choice(self.user_agents)
                
                # 添加更多随机头部
                random_headers = {
                    'Accept': random.choice([
                        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    ]),
                    'Accept-Language': random.choice([
                        'en-US,en;q=0.9',
                        'en-US,en;q=0.8',
                        'en-US,en;q=0.9,zh-CN;q=0.8',
                        'en-GB,en;q=0.9'
                    ]),
                    'Sec-CH-UA': random.choice([
                        '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                        '"Not_A Brand";v="8", "Chromium";v="119", "Google Chrome";v="119"',
                        '"Not_A Brand";v="8", "Chromium";v="118", "Google Chrome";v="118"'
                    ]),
                    'Sec-CH-UA-Mobile': '?0',
                    'Sec-CH-UA-Platform': random.choice(['"Windows"', '"macOS"', '"Linux"'])
                }
                
                # 更新随机头部
                self.session.headers.update(random_headers)
                
                # 发送请求
                response = self.session.get(url, timeout=30)
                
                # 检查响应状态
                if response.status_code == 200:
                    print(f"✅ 成功获取页面 (状态码: {response.status_code})")
                    return response
                elif response.status_code == 403:
                    print(f"❌ 被拒绝访问 (状态码: {response.status_code})")
                    # 尝试不同的策略
                    if attempt < max_retries - 1:
                        print("🔄 尝试不同的请求策略...")
                        self.try_alternative_request_strategy(url)
                elif response.status_code == 429:
                    print(f"⚠️ 请求过于频繁 (状态码: {response.status_code})")
                    wait_time = backoff_factor ** attempt * 10
                    print(f"⏳ 等待 {wait_time:.1f} 秒...")
                    time.sleep(wait_time)
                else:
                    print(f"⚠️ 意外状态码: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"⏰ 请求超时 (尝试 {attempt + 1})")
            except requests.exceptions.ConnectionError as e:
                print(f"🔌 连接错误 (尝试 {attempt + 1}): {e}")
            except Exception as e:
                print(f"❌ 其他错误 (尝试 {attempt + 1}): {e}")
            
            # 如果不是最后一次尝试，等待后重试
            if attempt < max_retries - 1:
                wait_time = backoff_factor ** attempt * random.uniform(3, 8)
                print(f"⏳ 等待 {wait_time:.1f} 秒后重试...")
                time.sleep(wait_time)
        
        print(f"❌ 所有尝试都失败了")
        return None
    
    def try_alternative_request_strategy(self, url):
        """尝试备选请求策略"""
        strategies = [
            self.strategy_google_cache,
            self.strategy_wayback_machine,
            self.strategy_mobile_user_agent,
            self.strategy_different_referer
        ]
        
        for strategy in strategies:
            try:
                result = strategy(url)
                if result:
                    return result
            except Exception as e:
                print(f"⚠️ 备选策略失败: {e}")
                continue
        
        return None
    
    def strategy_google_cache(self, url):
        """尝试通过Google缓存访问"""
        print("🔄 尝试Google缓存...")
        cache_url = f"https://webcache.googleusercontent.com/search?q=cache:{url}"
        try:
            response = self.session.get(cache_url, timeout=30)
            if response.status_code == 200:
                print("✅ Google缓存成功")
                return response
        except:
            pass
        return None
    
    def strategy_wayback_machine(self, url):
        """尝试通过Wayback Machine访问"""
        print("🔄 尝试Wayback Machine...")
        wayback_url = f"https://web.archive.org/web/{url}"
        try:
            response = self.session.get(wayback_url, timeout=30)
            if response.status_code == 200:
                print("✅ Wayback Machine成功")
                return response
        except:
            pass
        return None
    
    def strategy_mobile_user_agent(self, url):
        """尝试移动端User-Agent"""
        print("🔄 尝试移动端User-Agent...")
        mobile_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Android 14; Mobile; rv:109.0) Gecko/109.0 Firefox/121.0",
            "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        ]
        
        original_ua = self.session.headers.get('User-Agent')
        try:
            self.session.headers['User-Agent'] = random.choice(mobile_agents)
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                print("✅ 移动端User-Agent成功")
                return response
        except:
            pass
        finally:
            self.session.headers['User-Agent'] = original_ua
        return None
    
    def strategy_different_referer(self, url):
        """尝试不同的Referer"""
        print("🔄 尝试不同的Referer...")
        referers = [
            "https://www.google.com/",
            "https://www.bing.com/",
            "https://duckduckgo.com/",
            "https://www.reddit.com/",
            "https://twitter.com/",
            "https://www.facebook.com/"
        ]
        
        original_referer = self.session.headers.get('Referer')
        try:
            self.session.headers['Referer'] = random.choice(referers)
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                print("✅ 不同Referer成功")
                return response
        except:
            pass
        finally:
            if original_referer:
                self.session.headers['Referer'] = original_referer
            else:
                self.session.headers.pop('Referer', None)
        return None
    
    def extract_ai_tools_from_html(self, html_content, url):
        """从HTML内容中提取AI工具"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            tools = []
            
            # 针对theresanaiforthat.com的特殊选择器
            selectors = [
                # 常见的工具卡片选择器
                "div.tool-card",
                "div.tool-item",
                "div.ai-tool",
                "div[class*='tool']",
                "div[class*='card']",
                "div[class*='item']",
                "article",
                ".tool",
                ".card",
                ".item",
                "[data-tool]",
                "[data-item]",
                
                # 更通用的选择器
                "div.grid > div",
                "div.list > div",
                "div.container > div",
                "main > div",
                "section > div",
                
                # 链接相关的选择器
                "a[href*='tool']",
                "a[href*='app']",
                "a[href*='ai']",
                
                # 基于文本内容的选择器
                "div:contains('AI')",
                "div:contains('tool')",
                "div:contains('app')"
            ]
            
            print(f"🔍 尝试提取AI工具数据...")
            
            for selector in selectors:
                try:
                    # 跳过包含文本的选择器，BeautifulSoup不直接支持
                    if ':contains(' in selector:
                        continue
                        
                    elements = soup.select(selector)
                    if elements:
                        print(f"✅ 找到 {len(elements)} 个元素使用选择器: {selector}")
                        
                        for i, element in enumerate(elements[:30]):  # 限制最多30个
                            try:
                                tool_data = self.extract_tool_from_element(element, i + 1, url)
                                if tool_data:
                                    tools.append(tool_data)
                            except Exception as e:
                                print(f"⚠️ 提取工具 {i+1} 失败: {e}")
                                continue
                        
                        # 如果找到了工具，就不再尝试其他选择器
                        if tools:
                            break
                            
                except Exception as e:
                    print(f"⚠️ 选择器 {selector} 失败: {e}")
                    continue
            
            # 如果没有找到工具，尝试更通用的方法
            if not tools:
                print("🔄 尝试通用文本提取...")
                tools = self.extract_tools_generic(soup, url)
            
            print(f"📊 总共提取了 {len(tools)} 个AI工具")
            return tools
            
        except Exception as e:
            print(f"❌ 提取AI工具失败: {e}")
            return []
    
    def extract_tool_from_element(self, element, index, base_url):
        """从单个元素提取工具信息"""
        try:
            # 提取名称
            name = ""
            name_selectors = [
                "h1", "h2", "h3", "h4", "h5", "h6",
                ".title", ".name", ".tool-name", ".tool-title",
                "[class*='title']", "[class*='name']",
                "a", "strong", "b"
            ]
            
            for selector in name_selectors:
                try:
                    name_elem = element.select_one(selector)
                    if name_elem and name_elem.get_text().strip():
                        name = name_elem.get_text().strip()
                        break
                except:
                    continue
            
            # 提取描述
            description = ""
            desc_selectors = [
                ".description", ".desc", ".summary", ".info",
                "p", ".content", ".text", ".details",
                "[class*='desc']", "[class*='summary']"
            ]
            
            for selector in desc_selectors:
                try:
                    desc_elem = element.select_one(selector)
                    if desc_elem and desc_elem.get_text().strip():
                        description = desc_elem.get_text().strip()
                        break
                except:
                    continue
            
            # 提取链接
            link = ""
            try:
                link_elem = element.select_one("a[href]")
                if link_elem:
                    href = link_elem.get('href', '')
                    if href:
                        # 转换为绝对URL
                        link = urljoin(base_url, href)
            except:
                pass
            
            # 提取分类
            category = ""
            cat_selectors = [
                ".category", ".tag", ".type", ".genre",
                ".badge", ".label", "span"
            ]
            
            for selector in cat_selectors:
                try:
                    cat_elem = element.select_one(selector)
                    if cat_elem and cat_elem.get_text().strip():
                        category = cat_elem.get_text().strip()
                        break
                except:
                    continue
            
            # 验证数据质量
            if name and len(name.strip()) > 2:
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
            print(f"⚠️ 提取元素信息失败: {e}")
            return None
    
    def extract_tools_generic(self, soup, base_url):
        """通用的工具提取方法"""
        tools = []
        
        try:
            # 查找所有可能包含工具信息的元素
            all_links = soup.find_all('a', href=True)
            
            for i, link in enumerate(all_links[:100]):  # 限制检查前100个链接
                try:
                    href = link.get('href', '')
                    text = link.get_text().strip()
                    
                    # 过滤可能的工具链接
                    if (text and len(text) > 3 and 
                        any(keyword in text.lower() for keyword in ['ai', 'tool', 'app', 'platform', 'software']) and
                        not any(skip in href.lower() for skip in ['#', 'javascript:', 'mailto:', 'tel:'])):
                        
                        # 获取父元素的更多信息
                        parent = link.parent
                        description = ""
                        
                        # 尝试获取描述
                        if parent:
                            desc_text = parent.get_text().strip()
                            if desc_text and len(desc_text) > len(text):
                                description = desc_text
                        
                        tool_data = {
                            'name': text,
                            'description': description,
                            'link': urljoin(base_url, href),
                            'category': 'Unknown',
                            'source': 'theresanaiforthat.com',
                            'scraped_at': datetime.now().isoformat(),
                            'index': i + 1
                        }
                        
                        tools.append(tool_data)
                        
                except Exception as e:
                    continue
            
            return tools
            
        except Exception as e:
            print(f"❌ 通用提取失败: {e}")
            return []
    
    def scrape_ai_tools(self, url=None):
        """主要的爬取方法"""
        if not url:
            url = self.config.TARGET_URL
        
        print(f"🚀 开始爬取AI工具: {url}")
        
        # 获取网页内容
        response = self.get_with_retry(url)
        
        if response and response.status_code == 200:
            print("✅ 成功获取网页内容")
            
            # 提取AI工具数据
            tools = self.extract_ai_tools_from_html(response.text, url)
            
            if tools:
                print(f"🎉 成功提取 {len(tools)} 个AI工具")
                return tools
            else:
                print("❌ 没有提取到任何工具数据")
                return []
        else:
            print("❌ 无法获取网页内容")
            return [] 