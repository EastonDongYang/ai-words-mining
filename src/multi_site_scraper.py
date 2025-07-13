#!/usr/bin/env python3
"""
Multi-Site Scraper for AI Words Mining System
支持多个网站的AI工具和产品信息爬取
"""

import requests
import time
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config import Config
import json

class MultiSiteScraper:
    """Multi-site scraper for AI tools and products"""
    
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """Setup HTTP session with proper headers"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none'
        })
    
    def setup_driver(self) -> webdriver.Chrome:
        """Setup Chrome driver with anti-detection measures"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            # Get the driver path and fix it if needed
            driver_path = ChromeDriverManager().install()
            
            # Fix the common webdriver_manager path issue
            if driver_path.endswith('THIRD_PARTY_NOTICES.chromedriver'):
                import os
                driver_dir = os.path.dirname(driver_path)
                driver_path = os.path.join(driver_dir, 'chromedriver.exe')
                
                if not os.path.exists(driver_path):
                    # Try alternative path
                    driver_path = os.path.join(driver_dir, 'chromedriver')
            
            if self.config.DEBUG_MODE:
                print(f"Using Chrome driver: {driver_path}")
            
            service = webdriver.chrome.service.Service(driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return driver
            
        except Exception as e:
            print(f"Chrome driver setup failed: {e}")
            raise
    
    def scrape_all_sites(self) -> List[Dict]:
        """Scrape all configured sites and return combined results"""
        all_tools = []
        
        for url in self.config.TARGET_URLS:
            try:
                site_domain = urlparse(url).netloc
                site_config = self.config.get_site_config(site_domain)
                
                if not site_config.get('enabled', True):
                    continue
                
                print(f"🕷️ Scraping {site_domain}...")
                
                tools = self.scrape_site(url, site_config)
                
                if tools:
                    print(f"✅ Found {len(tools)} items from {site_domain}")
                    all_tools.extend(tools)
                else:
                    print(f"⚠️ No items found from {site_domain}")
                
                # Add delay between sites
                time.sleep(site_config.get('delay', 2))
                
            except Exception as e:
                print(f"❌ Error scraping {url}: {e}")
                continue
        
        # Remove duplicates based on name
        unique_tools = self.remove_duplicates(all_tools)
        
        print(f"📊 Total items collected: {len(unique_tools)} (after deduplication)")
        
        return unique_tools[:self.config.MAX_TOTAL_ITEMS]
    
    def scrape_site(self, url: str, site_config: dict) -> List[Dict]:
        """Scrape a specific site based on its configuration"""
        site_domain = urlparse(url).netloc
        
        # Route to specific scraper based on domain
        if 'toolify.ai' in site_domain:
            return self.scrape_toolify(url, site_config)
        elif 'producthunt.com' in site_domain:
            return self.scrape_producthunt(url, site_config)
        elif 'futuretools.io' in site_domain:
            return self.scrape_futuretools(url, site_config)
        elif 'betalist.com' in site_domain:
            return self.scrape_betalist(url, site_config)
        elif 'explodingtopics.com' in site_domain:
            return self.scrape_explodingtopics(url, site_config)
        else:
            return self.scrape_generic(url, site_config)
    
    def scrape_toolify(self, url: str, site_config: dict) -> List[Dict]:
        """Scrape Toolify.ai"""
        if not site_config.get('use_selenium', True):
            return self.scrape_toolify_requests(url, site_config)
        
        driver = None
        tools = []
        
        try:
            driver = self.setup_driver()
            driver.get(url)
            time.sleep(3)
            
            # Scroll to load more content
            for i in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Get page source and parse with BeautifulSoup
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find tool elements using BeautifulSoup
            elements = soup.find_all(class_='tool-item')
            
            if self.config.DEBUG_MODE:
                print(f"Found {len(elements)} tool items on Toolify")
            
            max_items = site_config.get('max_items', 50)
            for element in elements[:max_items]:
                try:
                    tool = self.extract_toolify_data(element)
                    if tool:
                        tools.append(tool)
                except Exception as e:
                    if self.config.DEBUG_MODE:
                        print(f"Error extracting tool: {e}")
                    continue
            
        except Exception as e:
            print(f"Error scraping Toolify: {e}")
        finally:
            if driver:
                driver.quit()
        
        return tools
    
    def scrape_producthunt(self, url: str, site_config: dict) -> List[Dict]:
        """Scrape Product Hunt"""
        driver = None
        tools = []
        
        try:
            driver = self.setup_driver()
            
            if self.config.DEBUG_MODE:
                print(f"Loading Product Hunt page: {url}")
                
            driver.get(url)
            time.sleep(5)  # 增加等待时间
            
            # Accept cookies if present
            try:
                cookie_button = driver.find_element(By.CSS_SELECTOR, '[data-test="cookie-banner-accept"]')
                if cookie_button:
                    cookie_button.click()
                    time.sleep(1)
            except:
                pass
            
            # 检查页面标题
            if self.config.DEBUG_MODE:
                print(f"Page title: {driver.title}")
            
            # Scroll to load more content
            for i in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Find product elements using the correct selector from debugging
            selectors = [
                '[data-test*="product"]',  # 调试发现的最佳选择器
                '[data-test*="item"]',
                'div[class*="styles_item"]',
                'div[class*="styles_product"]',
                'div[class*="item"]',
                'div[class*="card"]',
                'article',
                'li[class*="item"]'
            ]
            
            elements = []
            best_selector = None
            
            for selector in selectors:
                try:
                    found_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if found_elements and len(found_elements) > len(elements):
                        elements = found_elements
                        best_selector = selector
                        if self.config.DEBUG_MODE:
                            print(f"Found {len(elements)} elements with selector: {selector}")
                        if len(elements) >= 10:  # 找到足够的元素就停止
                            break
                except:
                    continue
            
            if not elements:
                if self.config.DEBUG_MODE:
                    print("No product elements found, trying fallback selectors...")
                # 尝试备用选择器
                fallback_selectors = ['div', 'li', 'article', 'section']
                for selector in fallback_selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        if len(elements) > 20:
                            elements = elements[:50]  # 限制数量
                            break
                    except:
                        continue
            
            if self.config.DEBUG_MODE:
                print(f"Total elements found: {len(elements)} using selector: {best_selector}")
            
            max_items = site_config.get('max_items', 25)
            for element in elements[:max_items]:
                try:
                    tool = self.extract_producthunt_data(element)
                    if tool:
                        tools.append(tool)
                except Exception as e:
                    if self.config.DEBUG_MODE:
                        print(f"Error extracting product data: {e}")
                    continue
            
            if self.config.DEBUG_MODE:
                print(f"Successfully extracted {len(tools)} products from Product Hunt")
            
        except Exception as e:
            print(f"Error scraping Product Hunt: {e}")
            if self.config.DEBUG_MODE:
                import traceback
                traceback.print_exc()
        finally:
            if driver:
                driver.quit()
        
        return tools
    
    def scrape_futuretools(self, url: str, site_config: dict) -> List[Dict]:
        """Scrape Future Tools"""
        driver = None
        tools = []
        
        try:
            driver = self.setup_driver()
            driver.get(url)
            time.sleep(3)
            
            # Scroll to load more content
            for i in range(2):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Find tool elements
            selectors = [
                '.tool-card', '.tool-item', '.tool',
                '[data-testid="tool-card"]',
                '.grid-item', '.card'
            ]
            
            elements = []
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(elements) > 5:
                        break
                except:
                    continue
            
            max_items = site_config.get('max_items', 40)
            for element in elements[:max_items]:
                try:
                    tool = self.extract_futuretools_data(element)
                    if tool:
                        tools.append(tool)
                except:
                    continue
            
        except Exception as e:
            print(f"Error scraping Future Tools: {e}")
        finally:
            if driver:
                driver.quit()
        
        return tools
    
    def scrape_betalist(self, url: str, site_config: dict) -> List[Dict]:
        """Scrape BetaList"""
        tools = []
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find startup elements
            elements = soup.find_all(['div', 'article'], class_=re.compile(r'startup|product|item'))
            
            max_items = site_config.get('max_items', 25)
            for element in elements[:max_items]:
                try:
                    tool = self.extract_betalist_data(element)
                    if tool:
                        tools.append(tool)
                except:
                    continue
            
        except Exception as e:
            print(f"Error scraping BetaList: {e}")
        
        return tools
    
    def scrape_explodingtopics(self, url: str, site_config: dict) -> List[Dict]:
        """Scrape Exploding Topics"""
        driver = None
        tools = []
        
        try:
            driver = self.setup_driver()
            driver.get(url)
            time.sleep(4)
            
            # Scroll to load more content
            for i in range(2):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            
            # Find topic elements
            selectors = [
                '.topic-card', '.topic-item', '.topic',
                '[data-testid="topic-card"]',
                '.trend-item', '.trend-card'
            ]
            
            elements = []
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(elements) > 3:
                        break
                except:
                    continue
            
            max_items = site_config.get('max_items', 20)
            for element in elements[:max_items]:
                try:
                    tool = self.extract_explodingtopics_data(element)
                    if tool:
                        tools.append(tool)
                except:
                    continue
            
        except Exception as e:
            print(f"Error scraping Exploding Topics: {e}")
        finally:
            if driver:
                driver.quit()
        
        return tools
    
    def scrape_generic(self, url: str, site_config: dict) -> List[Dict]:
        """Generic scraper for unknown sites"""
        tools = []
        
        try:
            if site_config.get('use_selenium', True):
                driver = self.setup_driver()
                driver.get(url)
                time.sleep(3)
                
                # Generic element selectors
                selectors = [
                    'article', '.card', '.item', '.product',
                    '.tool', '.app', '.service', '.startup'
                ]
                
                elements = []
                for selector in selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        if len(elements) > 3:
                            break
                    except:
                        continue
                
                max_items = site_config.get('max_items', 20)
                for element in elements[:max_items]:
                    try:
                        tool = self.extract_generic_data(element)
                        if tool:
                            tools.append(tool)
                    except:
                        continue
                
                driver.quit()
            else:
                # Use requests for simple sites
                response = self.session.get(url, timeout=30)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                elements = soup.find_all(['article', 'div'], class_=re.compile(r'card|item|product'))
                
                max_items = site_config.get('max_items', 20)
                for element in elements[:max_items]:
                    try:
                        tool = self.extract_generic_data_bs4(element)
                        if tool:
                            tools.append(tool)
                    except:
                        continue
            
        except Exception as e:
            print(f"Error in generic scraper: {e}")
        
        return tools
    
    def extract_toolify_data(self, element) -> Optional[Dict]:
        """Extract data from Toolify element"""
        try:
            # For Toolify.ai, extract from BeautifulSoup element (not Selenium)
            # The element structure contains tool name and description in text content
            
            # Get the text content of the entire element
            full_text = element.get_text(strip=True) if hasattr(element, 'get_text') else ""
            
            if not full_text or len(full_text) < 10:
                return None
            
            # Extract name and description from the text pattern
            # Format: "NameNameDescription..." or "Name Name Description..."
            
            # Try to find links to get the tool name
            name = ""
            description = ""
            
            # Method 1: Extract from links
            links = element.find_all('a') if hasattr(element, 'find_all') else []
            for link in links:
                href = link.get('href', '')
                link_text = link.get_text(strip=True)
                
                if href and href.startswith('/tool/') and link_text:
                    # Split the text to extract name and description
                    if len(link_text) > 10:
                        # Try to split at repeated words or common patterns
                        words = link_text.split()
                        
                        # Look for patterns like "NameNameDescription"
                        for i in range(1, min(len(words), 4)):
                            potential_name = ' '.join(words[:i])
                            potential_desc = ' '.join(words[i:])
                            
                            # Check if this looks like a reasonable split
                            if (len(potential_name) > 2 and len(potential_name) < 50 and
                                len(potential_desc) > 10 and len(potential_desc) < 300):
                                name = potential_name
                                description = potential_desc
                                break
                        
                        # If no good split found, use the first few words as name
                        if not name and len(words) >= 2:
                            name = ' '.join(words[:2])
                            description = ' '.join(words[2:]) if len(words) > 2 else ""
                        
                        break
            
            # Method 2: Fallback - extract from div content
            if not name:
                divs = element.find_all('div') if hasattr(element, 'find_all') else []
                for div in divs:
                    div_text = div.get_text(strip=True)
                    if div_text and len(div_text) > 10 and len(div_text) < 200:
                        words = div_text.split()
                        if len(words) >= 3:
                            name = ' '.join(words[:2])
                            description = ' '.join(words[2:])
                            break
            
            # Clean up the extracted data
            if name:
                # Remove duplicated words (common in Toolify structure)
                name_words = name.split()
                if len(name_words) >= 2 and name_words[0] == name_words[1]:
                    name = name_words[0]
                
                # Clean description
                if description:
                    # Remove the name from the beginning of description if it's duplicated
                    if description.lower().startswith(name.lower()):
                        description = description[len(name):].strip()
                
                # Extract categories from description or text
                categories = ['AI Tool']
                
                # Look for common AI categories in the text
                ai_keywords = ['AI', 'Machine Learning', 'Neural', 'GPT', 'LLM', 'Computer Vision', 
                              'NLP', 'Deep Learning', 'Automation', 'Generator', 'Assistant']
                
                text_lower = (name + ' ' + description).lower()
                for keyword in ai_keywords:
                    if keyword.lower() in text_lower:
                        categories.append(keyword)
                        if len(categories) >= 3:
                            break
                
                return {
                    'name': name.strip(),
                    'description': description.strip() or "AI tool from Toolify",
                    'categories': categories[:3],
                    'source': 'toolify.ai'
                }
            
        except Exception as e:
            if self.config.DEBUG_MODE:
                print(f"Error extracting Toolify data: {e}")
        
        return None
    
    def extract_producthunt_data(self, element) -> Optional[Dict]:
        """Extract data from Product Hunt element"""
        try:
            # 首先尝试获取完整文本
            full_text = element.text.strip()
            
            if self.config.DEBUG_MODE:
                print(f"Processing element with text: {full_text[:100]}...")
            
            # Product Hunt的格式通常是: "产品名称 — 产品描述"
            name = ""
            description = ""
            
            # 尝试从完整文本中解析产品名称和描述
            if full_text and len(full_text) > 5:
                # 检查是否包含 "—" 分隔符
                if " — " in full_text:
                    parts = full_text.split(" — ", 1)
                    if len(parts) >= 2:
                        name = parts[0].strip()
                        description = parts[1].strip()
                        
                        # 清理描述中的尾随内容
                        if description.endswith('...'):
                            description = description[:-3].strip()
                        
                        if self.config.DEBUG_MODE:
                            print(f"Parsed from full text - Name: {name}, Desc: {description[:50]}...")
                
                # 如果没有找到 "—" 分隔符，尝试其他方法
                if not name and len(full_text) > 0:
                    # 尝试从HTML元素中提取
                    name_selectors = [
                        "h3", "h4", "h2", "h1", "h5", "h6",
                        ".title", ".name", 
                        "[data-test*='name']", "[data-test*='title']",
                        "strong", "b", "a"
                    ]
                    
                    for selector in name_selectors:
                        try:
                            name_elem = element.find_element(By.CSS_SELECTOR, selector)
                            candidate_name = name_elem.text.strip()
                            
                            if candidate_name and len(candidate_name) > 2 and len(candidate_name) < 200:
                                # 排除干扰词汇
                                exclude_words = ['share', 'notify', 'coming soon', 'learn more', 'artificial intelligence', 'product hunt', 'read more']
                                if not any(word in candidate_name.lower() for word in exclude_words):
                                    name = candidate_name
                                    if self.config.DEBUG_MODE:
                                        print(f"Found name using selector {selector}: {name}")
                                    break
                        except:
                            continue
                    
                    # 如果还是没有找到名称，尝试从完整文本的第一行提取
                    if not name:
                        lines = full_text.split('\n')
                        if lines:
                            first_line = lines[0].strip()
                            if first_line and len(first_line) > 2 and len(first_line) < 200:
                                # 如果第一行包含 "—"，只取前半部分
                                if " — " in first_line:
                                    name = first_line.split(" — ")[0].strip()
                                else:
                                    name = first_line
                                
                                if self.config.DEBUG_MODE:
                                    print(f"Extracted name from first line: {name}")
                    
                    # 如果没有描述，尝试从HTML元素中提取
                    if not description:
                        desc_selectors = [
                            "p", ".description", ".desc", ".summary", ".tagline",
                            "[data-test*='description']", "[data-test*='desc']",
                            "span", "div"
                        ]
                        
                        for selector in desc_selectors:
                            try:
                                desc_elements = element.find_elements(By.CSS_SELECTOR, selector)
                                for desc_elem in desc_elements:
                                    candidate_desc = desc_elem.text.strip()
                                    
                                    if candidate_desc and len(candidate_desc) > 10 and len(candidate_desc) < 500:
                                        # 排除干扰词汇和重复的名称
                                        exclude_words = ['share', 'notify me', 'coming soon', 'learn more', 'read more', 'click here']
                                        if not any(word in candidate_desc.lower() for word in exclude_words):
                                            if candidate_desc != name:  # 描述不应该和名称相同
                                                description = candidate_desc
                                                if self.config.DEBUG_MODE:
                                                    print(f"Found description: {description[:50]}...")
                                                break
                                if description:
                                    break
                            except:
                                continue
                        
                        # 如果还是没有描述，尝试从完整文本的其他部分提取
                        if not description and len(full_text) > len(name) + 10:
                            # 尝试从 "—" 后面的内容提取
                            if " — " in full_text:
                                desc_part = full_text.split(" — ", 1)[1].strip()
                                if desc_part:
                                    description = desc_part
                            else:
                                # 尝试从换行后的内容提取
                                lines = full_text.split('\n')
                                if len(lines) > 1:
                                    for line in lines[1:]:
                                        line = line.strip()
                                        if line and len(line) > 10:
                                            description = line
                                            break
            
            # 验证数据质量
            if not name or len(name) < 2:
                if self.config.DEBUG_MODE:
                    print(f"Skipping - invalid name: '{name}'")
                return None
            
            # 清理名称中的特殊字符
            name = name.replace('—', '-').replace('–', '-').strip()
            
            # 如果没有描述，设置默认值
            if not description:
                description = "Product description not available"
                
            # 清理描述
            description = description.replace('...', '').strip()
            
            # 提取类别
            categories = ['Product Hunt']
            
            # 尝试提取链接
            link = ""
            try:
                link_elem = element.find_element(By.CSS_SELECTOR, "a")
                link = link_elem.get_attribute("href")
                if link and not link.startswith('http'):
                    link = f"https://www.producthunt.com{link}"
            except:
                pass
            
            if self.config.DEBUG_MODE:
                print(f"Successfully extracted: {name} - {description[:50]}...")
            
            return {
                'name': name,
                'description': description,
                'categories': categories,
                'link': link,
                'source': 'producthunt.com'
            }
            
        except Exception as e:
            if self.config.DEBUG_MODE:
                print(f"Error extracting Product Hunt data: {e}")
        
        return None
    
    def extract_futuretools_data(self, element) -> Optional[Dict]:
        """Extract data from Future Tools element"""
        try:
            # Extract name
            name = ""
            for selector in ["h3", "h4", ".title", ".name"]:
                try:
                    name_elem = element.find_element(By.CSS_SELECTOR, selector)
                    name = name_elem.text.strip()
                    if name and len(name) > 2:
                        break
                except:
                    continue
            
            # Extract description
            description = ""
            for selector in ["p", ".description", ".desc"]:
                try:
                    desc_elem = element.find_element(By.CSS_SELECTOR, selector)
                    description = desc_elem.text.strip()
                    if description and len(description) > 10:
                        break
                except:
                    continue
            
            if name and len(name) > 2:
                return {
                    'name': name,
                    'description': description or "Future Tools description not available",
                    'categories': ['Future Tools'],
                    'source': 'futuretools.io'
                }
            
        except Exception as e:
            if self.config.DEBUG_MODE:
                print(f"Error extracting Future Tools data: {e}")
        
        return None
    
    def extract_betalist_data(self, element) -> Optional[Dict]:
        """Extract data from BetaList element"""
        try:
            # Extract name - try multiple strategies
            name = ""
            
            # Strategy 1: Look for specific BetaList selectors
            name_selectors = [
                'h2', 'h3', 'h4', 'h5',
                '.startup-name', '.title', '.name',
                'a[href*="startup"]', 'strong', 'b'
            ]
            
            for selector in name_selectors:
                try:
                    if selector.startswith('.') or selector.startswith('['):
                        name_elem = element.select_one(selector)
                    else:
                        name_elem = element.find(selector)
                    
                    if name_elem:
                        name = name_elem.get_text(strip=True)
                        if name and len(name) > 2 and len(name) < 100:
                            break
                except:
                    continue
            
            # Strategy 2: Look in links
            if not name:
                links = element.find_all('a')
                for link in links:
                    link_text = link.get_text(strip=True)
                    if link_text and len(link_text) > 2 and len(link_text) < 100:
                        # Skip common navigation texts
                        skip_texts = ['read more', 'more', 'learn more', 'visit', 'website', 'startup', 'home']
                        if not any(skip in link_text.lower() for skip in skip_texts):
                            name = link_text
                            break
            
            # Extract description
            description = ""
            desc_selectors = [
                'p', '.description', '.desc', '.summary', '.tagline',
                '.startup-description', 'span', 'div'
            ]
            
            for selector in desc_selectors:
                try:
                    if selector.startswith('.'):
                        desc_elem = element.select_one(selector)
                    else:
                        desc_elem = element.find(selector)
                    
                    if desc_elem:
                        desc_text = desc_elem.get_text(strip=True)
                        if desc_text and len(desc_text) > 10 and len(desc_text) < 500:
                            description = desc_text
                            break
                except:
                    continue
            
            # Extract tags/categories if available
            categories = ['BetaList', 'Startup']
            try:
                tag_elements = element.find_all(['span', 'div'], class_=re.compile(r'tag|category|label'))
                for tag in tag_elements:
                    tag_text = tag.get_text(strip=True)
                    if tag_text and len(tag_text) < 30:
                        categories.append(tag_text)
            except:
                pass
            
            if name and len(name) > 2:
                return {
                    'name': name,
                    'description': description or "BetaList startup description not available",
                    'categories': categories[:5],  # Limit to 5 categories
                    'source': 'betalist.com'
                }
            
        except Exception as e:
            if self.config.DEBUG_MODE:
                print(f"Error extracting BetaList data: {e}")
        
        return None
    
    def extract_explodingtopics_data(self, element) -> Optional[Dict]:
        """Extract data from Exploding Topics element"""
        try:
            # Extract name
            name = ""
            for selector in ["h3", "h4", ".title", ".topic-name"]:
                try:
                    name_elem = element.find_element(By.CSS_SELECTOR, selector)
                    name = name_elem.text.strip()
                    if name and len(name) > 2:
                        break
                except:
                    continue
            
            # Extract description or trend info
            description = ""
            for selector in ["p", ".description", ".trend-info"]:
                try:
                    desc_elem = element.find_element(By.CSS_SELECTOR, selector)
                    description = desc_elem.text.strip()
                    if description and len(description) > 10:
                        break
                except:
                    continue
            
            if name and len(name) > 2:
                return {
                    'name': name,
                    'description': description or "Trending AI topic",
                    'categories': ['Exploding Topics', 'Trend'],
                    'source': 'explodingtopics.com'
                }
            
        except Exception as e:
            if self.config.DEBUG_MODE:
                print(f"Error extracting Exploding Topics data: {e}")
        
        return None
    
    def extract_generic_data(self, element) -> Optional[Dict]:
        """Extract data from generic element using Selenium"""
        try:
            # Extract name
            name = ""
            for selector in ["h1", "h2", "h3", "h4", ".title", ".name"]:
                try:
                    name_elem = element.find_element(By.CSS_SELECTOR, selector)
                    name = name_elem.text.strip()
                    if name and len(name) > 2:
                        break
                except:
                    continue
            
            # Extract description
            description = ""
            for selector in ["p", ".description", ".desc"]:
                try:
                    desc_elem = element.find_element(By.CSS_SELECTOR, selector)
                    description = desc_elem.text.strip()
                    if description and len(description) > 10:
                        break
                except:
                    continue
            
            if name and len(name) > 2:
                return {
                    'name': name,
                    'description': description or "Generic description not available",
                    'categories': ['Generic'],
                    'source': 'generic'
                }
            
        except Exception as e:
            if self.config.DEBUG_MODE:
                print(f"Error extracting generic data: {e}")
        
        return None
    
    def extract_generic_data_bs4(self, element) -> Optional[Dict]:
        """Extract data from generic element using BeautifulSoup"""
        try:
            # Extract name
            name = ""
            name_elem = element.find(['h1', 'h2', 'h3', 'h4'], class_=re.compile(r'title|name'))
            if name_elem:
                name = name_elem.get_text(strip=True)
            
            # Extract description
            description = ""
            desc_elem = element.find(['p', 'div'], class_=re.compile(r'description|desc'))
            if desc_elem:
                description = desc_elem.get_text(strip=True)
            
            if name and len(name) > 2:
                return {
                    'name': name,
                    'description': description or "Generic description not available",
                    'categories': ['Generic'],
                    'source': 'generic'
                }
            
        except Exception as e:
            if self.config.DEBUG_MODE:
                print(f"Error extracting generic BS4 data: {e}")
        
        return None
    
    def remove_duplicates(self, tools: List[Dict]) -> List[Dict]:
        """Remove duplicate tools based on name similarity"""
        unique_tools = []
        seen_names = set()
        
        for tool in tools:
            name = tool.get('name', '').lower().strip()
            if name and name not in seen_names:
                seen_names.add(name)
                unique_tools.append(tool)
        
        return unique_tools
    
    def scrape_toolify_requests(self, url: str, site_config: dict) -> List[Dict]:
        """Fallback scraper for Toolify using requests"""
        tools = []
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find tool elements
            elements = soup.find_all(['div', 'article'], class_=re.compile(r'tool|card|item'))
            
            max_items = site_config.get('max_items', 50)
            for element in elements[:max_items]:
                try:
                    tool = self.extract_generic_data_bs4(element)
                    if tool:
                        tool['source'] = 'toolify.ai'
                        tools.append(tool)
                except:
                    continue
            
        except Exception as e:
            print(f"Error in Toolify requests scraper: {e}")
        
        return tools
    
    def save_results(self, tools: List[Dict], filename: str = "multi_site_scraped_tools.json"):
        """Save scraping results to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(tools, f, indent=2, ensure_ascii=False)
            print(f"✅ Results saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {e}") 