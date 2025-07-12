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
        
        driver = webdriver.Chrome(
            service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
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
            
            # Find tool elements
            selectors = [
                '.tool-card', '[data-testid="tool-card"]', '.ai-tool-card',
                '.grid-item', '.tool-item', '.tool', 'article', '.card'
            ]
            
            elements = []
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(elements) > 5:
                        break
                except:
                    continue
            
            max_items = site_config.get('max_items', 50)
            for element in elements[:max_items]:
                try:
                    tool = self.extract_toolify_data(element)
                    if tool:
                        tools.append(tool)
                except:
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
            driver.get(url)
            time.sleep(4)
            
            # Accept cookies if present
            try:
                cookie_button = driver.find_element(By.CSS_SELECTOR, '[data-test="cookie-banner-accept"]')
                if cookie_button:
                    cookie_button.click()
                    time.sleep(1)
            except:
                pass
            
            # Scroll to load more content
            for i in range(2):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            
            # Find product elements
            selectors = [
                '[data-test="homepage-section-item"]',
                '[data-test="product-item"]',
                '.styles_item__1Z1Sy',
                '.styles_productItem__1ZzOE'
            ]
            
            elements = []
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(elements) > 3:
                        break
                except:
                    continue
            
            max_items = site_config.get('max_items', 30)
            for element in elements[:max_items]:
                try:
                    tool = self.extract_producthunt_data(element)
                    if tool:
                        tools.append(tool)
                except:
                    continue
            
        except Exception as e:
            print(f"Error scraping Product Hunt: {e}")
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
            for selector in ["p", ".description", ".desc", ".summary"]:
                try:
                    desc_elem = element.find_element(By.CSS_SELECTOR, selector)
                    description = desc_elem.text.strip()
                    if description and len(description) > 10:
                        break
                except:
                    continue
            
            # Extract categories
            categories = []
            try:
                tag_elements = element.find_elements(By.CSS_SELECTOR, ".tag, .category, .badge")
                for tag in tag_elements:
                    tag_text = tag.text.strip()
                    if tag_text:
                        categories.append(tag_text)
            except:
                pass
            
            if name and len(name) > 2:
                return {
                    'name': name,
                    'description': description or "AI tool description not available",
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
            # Extract name
            name = ""
            for selector in ["h3", "h4", ".title", "[data-test='product-name']"]:
                try:
                    name_elem = element.find_element(By.CSS_SELECTOR, selector)
                    name = name_elem.text.strip()
                    if name and len(name) > 2:
                        break
                except:
                    continue
            
            # Extract description
            description = ""
            for selector in ["p", ".description", "[data-test='product-description']"]:
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
                    'description': description or "Product description not available",
                    'categories': ['Product Hunt'],
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
            # Extract name
            name = ""
            name_elem = element.find(['h2', 'h3', 'h4'], class_=re.compile(r'title|name'))
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
                    'description': description or "BetaList startup description not available",
                    'categories': ['BetaList', 'Startup'],
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