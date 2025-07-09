import requests
import time
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config import Config
import json
import re

class ToolifyScraper:
    """Scraper specifically designed for toolify.ai"""
    
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
    def setup_driver(self) -> webdriver.Chrome:
        """Setup Chrome driver for Toolify.ai"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        driver = webdriver.Chrome(
            service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Execute script to remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def scrape_with_selenium(self, url: str) -> List[Dict]:
        """Scrape Toolify.ai using Selenium"""
        tools_data = []
        driver = None
        
        try:
            driver = self.setup_driver()
            
            if self.config.DEBUG_MODE:
                print(f"Loading Toolify.ai page: {url}")
            
            driver.get(url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Scroll to load more content
            for i in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Try different selectors for Toolify.ai tool cards
            possible_selectors = [
                '.tool-card',
                '[data-testid="tool-card"]',
                '.ai-tool-card',
                '.grid-item',
                '.tool-item',
                '.tool',
                'article',
                '.card',
                'div[class*="tool"]',
                'div[class*="card"]'
            ]
            
            tool_elements = []
            for selector in possible_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and len(elements) > 5:  # Should have multiple tools
                        tool_elements = elements
                        if self.config.DEBUG_MODE:
                            print(f"Found {len(tool_elements)} tools with selector: {selector}")
                        break
                except:
                    continue
            
            if not tool_elements:
                # Fallback: try to find any links or divs that might contain tools
                tool_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='tool'], div[class*='grid'] > div")
                if self.config.DEBUG_MODE:
                    print(f"Fallback: Found {len(tool_elements)} potential tool elements")
            
            for element in tool_elements[:50]:  # Limit to 50 tools
                try:
                    tool_data = self.extract_tool_data_selenium(element)
                    if tool_data and tool_data['name'] and tool_data['name'] != "Unknown":
                        tools_data.append(tool_data)
                except Exception as e:
                    if self.config.DEBUG_MODE:
                        print(f"Error extracting tool data: {e}")
                    continue
            
            return tools_data
            
        except Exception as e:
            print(f"Error scraping Toolify.ai with Selenium: {e}")
            return []
        finally:
            if driver:
                driver.quit()
    
    def extract_tool_data_selenium(self, element) -> Optional[Dict]:
        """Extract tool data from a single element using Selenium"""
        try:
            # Extract tool name - try multiple strategies
            name = ""
            name_selectors = [
                "h1", "h2", "h3", "h4", "h5", "h6",
                ".title", ".name", ".tool-name",
                "[data-testid*='name']", "[data-testid*='title']",
                "a", ".link"
            ]
            
            for selector in name_selectors:
                try:
                    name_element = element.find_element(By.CSS_SELECTOR, selector)
                    name = name_element.text.strip()
                    if name and len(name) > 2 and len(name) < 100:
                        break
                except:
                    continue
            
            # Extract description
            description = ""
            desc_selectors = [
                "p", ".description", ".desc", ".summary",
                "[data-testid*='desc']", ".content", ".text"
            ]
            
            for selector in desc_selectors:
                try:
                    desc_element = element.find_element(By.CSS_SELECTOR, selector)
                    description = desc_element.text.strip()
                    if description and len(description) > 10:
                        break
                except:
                    continue
            
            # Extract categories/tags
            categories = []
            tag_selectors = [
                ".tag", ".category", ".badge", ".label",
                "[data-testid*='tag']", "[data-testid*='category']",
                ".chip", ".pill"
            ]
            
            for selector in tag_selectors:
                try:
                    tag_elements = element.find_elements(By.CSS_SELECTOR, selector)
                    for tag in tag_elements:
                        tag_text = tag.text.strip()
                        if tag_text and len(tag_text) < 30:
                            categories.append(tag_text)
                except:
                    continue
            
            # Extract link
            link = ""
            try:
                link_element = element.find_element(By.CSS_SELECTOR, "a")
                link = link_element.get_attribute("href") or ""
                if link and not link.startswith('http'):
                    link = f"https://www.toolify.ai{link}"
            except:
                pass
            
            # Only return if we have a valid name and description
            if not name or name == "Unknown" or len(name) < 3:
                return None
                
            if not description:
                description = "AI tool description not available"
            
            return {
                'name': name,
                'description': description,
                'categories': categories[:5],  # Limit categories
                'link': link,
                'source': 'toolify.ai',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            if self.config.DEBUG_MODE:
                print(f"Error extracting tool data from element: {e}")
            return None
    
    def scrape_with_requests(self, url: str) -> List[Dict]:
        """Fallback scraping method using requests"""
        tools_data = []
        
        try:
            if self.config.DEBUG_MODE:
                print(f"Scraping Toolify.ai with requests: {url}")
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Try to find tool containers
            possible_selectors = [
                'div[class*="tool"]',
                'div[class*="card"]',
                'article',
                'div[class*="grid"] > div',
                'a[href*="tool"]'
            ]
            
            tool_elements = []
            for selector in possible_selectors:
                elements = soup.select(selector)
                if elements and len(elements) > 5:
                    tool_elements = elements
                    if self.config.DEBUG_MODE:
                        print(f"Found {len(tool_elements)} tools with selector: {selector}")
                    break
            
            for element in tool_elements[:50]:
                tool_data = self.extract_tool_data_bs4(element)
                if tool_data and tool_data['name'] and tool_data['name'] != "Unknown":
                    tools_data.append(tool_data)
            
            return tools_data
            
        except Exception as e:
            print(f"Error scraping Toolify.ai with requests: {e}")
            return []
    
    def extract_tool_data_bs4(self, element) -> Optional[Dict]:
        """Extract tool data using BeautifulSoup"""
        try:
            # Extract name
            name = ""
            name_elements = element.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a'])
            for elem in name_elements:
                text = elem.get_text(strip=True)
                if text and len(text) > 2 and len(text) < 100:
                    name = text
                    break
            
            # Extract description
            description = ""
            desc_elements = element.find_all('p')
            for elem in desc_elements:
                text = elem.get_text(strip=True)
                if text and len(text) > 10:
                    description = text
                    break
            
            # Extract categories
            categories = []
            tag_elements = element.find_all(['span', 'div'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['tag', 'category', 'badge', 'label', 'chip']
            ))
            for tag in tag_elements:
                tag_text = tag.get_text(strip=True)
                if tag_text and len(tag_text) < 30:
                    categories.append(tag_text)
            
            # Extract link
            link = ""
            link_elem = element.find('a')
            if link_elem:
                link = link_elem.get('href', '')
                if link and not link.startswith('http'):
                    link = f"https://www.toolify.ai{link}"
            
            if not name or len(name) < 3:
                return None
                
            if not description:
                description = "AI tool description not available"
            
            return {
                'name': name,
                'description': description,
                'categories': categories[:5],
                'link': link,
                'source': 'toolify.ai',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            return None
    
    def scrape(self, url: str = None) -> List[Dict]:
        """Main scraping method"""
        if not url:
            url = self.config.TARGET_URL
        
        print(f"🕷️ Starting to scrape Toolify.ai: {url}")
        
        # Try Selenium first
        tools_data = self.scrape_with_selenium(url)
        
        # If Selenium failed or returned few results, try requests
        if len(tools_data) < 5:
            print("🔄 Selenium returned few results, trying requests method...")
            tools_data.extend(self.scrape_with_requests(url))
        
        # Remove duplicates
        seen_names = set()
        unique_tools = []
        for tool in tools_data:
            if tool['name'] not in seen_names:
                seen_names.add(tool['name'])
                unique_tools.append(tool)
        
        print(f"✅ Successfully scraped {len(unique_tools)} unique AI tools from Toolify.ai")
        
        if self.config.DEBUG_MODE and unique_tools:
            print("Sample tools found:")
            for tool in unique_tools[:3]:
                print(f"  - {tool['name']}: {tool['description'][:100]}...")
        
        return unique_tools
    
    def save_to_json(self, tools_data: List[Dict], filename: str = "toolify_scraped_tools.json"):
        """Save scraped data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(tools_data, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {len(tools_data)} tools to {filename}")
        except Exception as e:
            print(f"❌ Error saving to JSON: {e}") 