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

class AIToolsScraper:
    """Scraper for theresanaiforthat.com"""
    
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def setup_driver(self) -> webdriver.Chrome:
        """Setup Chrome driver for dynamic content scraping"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        driver = webdriver.Chrome(
            service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        return driver
    
    def scrape_with_selenium(self, url: str) -> List[Dict]:
        """Scrape AI tools data using Selenium for dynamic content"""
        tools_data = []
        driver = None
        
        try:
            driver = self.setup_driver()
            
            if self.config.DEBUG_MODE:
                print(f"Loading page: {url}")
            
            driver.get(url)
            
            # Wait for the page to load
            wait = WebDriverWait(driver, 10)
            
            # Wait for tool cards to load
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tool-card']")))
            
            # Scroll to load more content if needed
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Find all tool cards
            tool_cards = driver.find_elements(By.CSS_SELECTOR, "[data-testid='tool-card']")
            
            if self.config.DEBUG_MODE:
                print(f"Found {len(tool_cards)} tool cards")
            
            for card in tool_cards:
                try:
                    tool_data = self.extract_tool_data_selenium(card)
                    if tool_data:
                        tools_data.append(tool_data)
                except Exception as e:
                    if self.config.DEBUG_MODE:
                        print(f"Error extracting tool data: {e}")
                    continue
            
            return tools_data
            
        except Exception as e:
            print(f"Error scraping with Selenium: {e}")
            return []
        finally:
            if driver:
                driver.quit()
    
    def extract_tool_data_selenium(self, card) -> Optional[Dict]:
        """Extract tool data from a single tool card using Selenium"""
        try:
            # Extract tool name
            name_element = card.find_element(By.CSS_SELECTOR, "h3, .tool-name, [data-testid='tool-name']")
            name = name_element.text.strip() if name_element else "Unknown"
            
            # Extract description
            desc_element = card.find_element(By.CSS_SELECTOR, "p, .description, [data-testid='tool-description']")
            description = desc_element.text.strip() if desc_element else "No description"
            
            # Extract categories/tags
            categories = []
            try:
                tag_elements = card.find_elements(By.CSS_SELECTOR, ".tag, .category, [data-testid='tool-tag']")
                categories = [tag.text.strip() for tag in tag_elements if tag.text.strip()]
            except:
                pass
            
            # Extract link
            link = ""
            try:
                link_element = card.find_element(By.CSS_SELECTOR, "a")
                link = link_element.get_attribute("href") or ""
            except:
                pass
            
            # Extract rating/popularity if available
            rating = ""
            try:
                rating_element = card.find_element(By.CSS_SELECTOR, ".rating, .score, [data-testid='tool-rating']")
                rating = rating_element.text.strip()
            except:
                pass
            
            return {
                'name': name,
                'description': description,
                'categories': categories,
                'link': link,
                'rating': rating,
                'source': 'theresanaiforthat.com',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            if self.config.DEBUG_MODE:
                print(f"Error extracting tool data from card: {e}")
            return None
    
    def scrape_with_requests(self, url: str) -> List[Dict]:
        """Fallback scraping method using requests and BeautifulSoup"""
        tools_data = []
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try different possible selectors for tool cards
            possible_selectors = [
                '.tool-card',
                '.ai-tool',
                '[data-testid="tool-card"]',
                '.grid-item',
                '.tool-item'
            ]
            
            tool_cards = []
            for selector in possible_selectors:
                tool_cards = soup.select(selector)
                if tool_cards:
                    break
            
            if self.config.DEBUG_MODE:
                print(f"Found {len(tool_cards)} tool cards with requests method")
            
            for card in tool_cards:
                tool_data = self.extract_tool_data_bs4(card)
                if tool_data:
                    tools_data.append(tool_data)
            
            return tools_data
            
        except Exception as e:
            print(f"Error scraping with requests: {e}")
            return []
    
    def extract_tool_data_bs4(self, card) -> Optional[Dict]:
        """Extract tool data from a single tool card using BeautifulSoup"""
        try:
            # Extract tool name
            name_element = card.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            name = name_element.get_text(strip=True) if name_element else "Unknown"
            
            # Extract description
            desc_element = card.find('p')
            description = desc_element.get_text(strip=True) if desc_element else "No description"
            
            # Extract categories/tags
            categories = []
            tag_elements = card.find_all(['span', 'div'], class_=lambda x: x and ('tag' in x.lower() or 'category' in x.lower()))
            categories = [tag.get_text(strip=True) for tag in tag_elements if tag.get_text(strip=True)]
            
            # Extract link
            link = ""
            link_element = card.find('a')
            if link_element:
                link = link_element.get('href', '')
                if link and not link.startswith('http'):
                    link = f"https://theresanaiforthat.com{link}"
            
            return {
                'name': name,
                'description': description,
                'categories': categories,
                'link': link,
                'rating': '',
                'source': 'theresanaiforthat.com',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            if self.config.DEBUG_MODE:
                print(f"Error extracting tool data from card: {e}")
            return None
    
    def scrape(self, url: str = None) -> List[Dict]:
        """Main scraping method that tries different approaches"""
        if not url:
            url = self.config.TARGET_URL
        
        print(f"Starting to scrape: {url}")
        
        # Try Selenium first for dynamic content
        tools_data = self.scrape_with_selenium(url)
        
        # If Selenium fails or returns no data, try requests
        if not tools_data:
            print("Selenium scraping failed, trying requests method...")
            tools_data = self.scrape_with_requests(url)
        
        # Remove duplicates based on name
        unique_tools = {}
        for tool in tools_data:
            if tool['name'] not in unique_tools:
                unique_tools[tool['name']] = tool
        
        final_tools = list(unique_tools.values())
        
        print(f"Successfully scraped {len(final_tools)} unique AI tools")
        
        if self.config.DEBUG_MODE:
            print("Sample scraped data:")
            for i, tool in enumerate(final_tools[:3]):  # Show first 3 tools
                print(f"{i+1}. {tool['name']}: {tool['description'][:100]}...")
        
        return final_tools
    
    def save_to_json(self, tools_data: List[Dict], filename: str = "scraped_tools.json"):
        """Save scraped data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(tools_data, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(tools_data)} tools to {filename}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")

if __name__ == "__main__":
    scraper = AIToolsScraper()
    tools = scraper.scrape()
    scraper.save_to_json(tools) 