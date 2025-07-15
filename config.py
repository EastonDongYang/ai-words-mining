import os
from dotenv import load_dotenv
from typing import Optional, List

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the AI Words Mining System"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    
    # Google Sheets Configuration (removed - using backup outputs only)
    
    # Scraping Configuration
    TARGET_URL: str = os.getenv('TARGET_URL', 'https://www.toolify.ai/new')
    
    # Multiple Target URLs for comprehensive data collection
    TARGET_URLS: List[str] = [
        'https://www.toolify.ai/new',
        'https://www.producthunt.com/coming-soon?ref=header_nav',
        'https://www.producthunt.com/topics/artificial-intelligence?order=most_recent',
        'https://www.futuretools.io/newly-added',
        'https://betalist.com/',
        'https://explodingtopics.com/ai-topics-last-2-years-by-growth'
    ]
    
    # Site-specific configuration
    SITE_CONFIGS: dict = {
        'toolify.ai': {
            'enabled': True,
            'max_items': 30,  # 增加数量
            'delay': 2,
            'use_selenium': True
        },
        'producthunt.com': {
            'enabled': True,
            'max_items': 25,  # 增加数量
            'delay': 3,
            'use_selenium': True
        },
        'futuretools.io': {
            'enabled': True,  # 启用Future Tools
            'max_items': 25,
            'delay': 2,
            'use_selenium': True
        },
        'betalist.com': {
            'enabled': True,
            'max_items': 20,  # 增加数量
            'delay': 2,
            'use_selenium': False
        },
        'explodingtopics.com': {
            'enabled': True,  # 启用Exploding Topics
            'max_items': 15,
            'delay': 3,
            'use_selenium': True
        }
    }
    
    SCRAPING_DELAY: int = int(os.getenv('SCRAPING_DELAY', '2'))
    
    # Crawl4AI Configuration
    USE_CRAWL4AI: bool = os.getenv('USE_CRAWL4AI', 'true').lower() == 'true'
    CRAWL4AI_HEADLESS: bool = os.getenv('CRAWL4AI_HEADLESS', 'true').lower() == 'true'
    CRAWL4AI_VERBOSE: bool = os.getenv('CRAWL4AI_VERBOSE', 'false').lower() == 'true'
    CRAWL4AI_CACHE_MODE: str = os.getenv('CRAWL4AI_CACHE_MODE', 'enabled')  # enabled, disabled, bypass
    CRAWL4AI_MAX_CONCURRENT: int = int(os.getenv('CRAWL4AI_MAX_CONCURRENT', '5'))
    CRAWL4AI_BROWSER_TYPE: str = os.getenv('CRAWL4AI_BROWSER_TYPE', 'chromium')  # chromium, firefox, webkit
    CRAWL4AI_USER_AGENT: str = os.getenv('CRAWL4AI_USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    CRAWL4AI_VIEWPORT_WIDTH: int = int(os.getenv('CRAWL4AI_VIEWPORT_WIDTH', '1920'))
    CRAWL4AI_VIEWPORT_HEIGHT: int = int(os.getenv('CRAWL4AI_VIEWPORT_HEIGHT', '1080'))
    CRAWL4AI_WAIT_TIMEOUT: int = int(os.getenv('CRAWL4AI_WAIT_TIMEOUT', '30000'))
    CRAWL4AI_ENABLE_SCREENSHOTS: bool = os.getenv('CRAWL4AI_ENABLE_SCREENSHOTS', 'false').lower() == 'true'
    CRAWL4AI_ENABLE_NETWORK_CAPTURE: bool = os.getenv('CRAWL4AI_ENABLE_NETWORK_CAPTURE', 'false').lower() == 'true'
    
    # LLM Extraction Configuration
    ENABLE_LLM_EXTRACTION: bool = os.getenv('ENABLE_LLM_EXTRACTION', 'false').lower() == 'true'
    LLM_PROVIDER: str = os.getenv('LLM_PROVIDER', 'openai/gpt-4o-mini')  # openai/gpt-4o-mini, anthropic/claude-3-haiku, etc.
    LLM_MAX_TOKENS: int = int(os.getenv('LLM_MAX_TOKENS', '4000'))
    LLM_TEMPERATURE: float = float(os.getenv('LLM_TEMPERATURE', '0.1'))
    
    # Content Filtering Configuration
    CONTENT_FILTER_TYPE: str = os.getenv('CONTENT_FILTER_TYPE', 'pruning')  # pruning, bm25, none
    CONTENT_FILTER_THRESHOLD: float = float(os.getenv('CONTENT_FILTER_THRESHOLD', '0.48'))
    CONTENT_FILTER_MIN_WORDS: int = int(os.getenv('CONTENT_FILTER_MIN_WORDS', '10'))
    BM25_QUERY: str = os.getenv('BM25_QUERY', 'AI tools artificial intelligence machine learning')
    BM25_THRESHOLD: float = float(os.getenv('BM25_THRESHOLD', '1.0'))
    
    # Deep Crawling Configuration
    ENABLE_DEEP_CRAWL: bool = os.getenv('ENABLE_DEEP_CRAWL', 'false').lower() == 'true'
    DEEP_CRAWL_STRATEGY: str = os.getenv('DEEP_CRAWL_STRATEGY', 'bfs')  # bfs, dfs, bestfirst
    DEEP_CRAWL_MAX_DEPTH: int = int(os.getenv('DEEP_CRAWL_MAX_DEPTH', '3'))
    DEEP_CRAWL_MAX_PAGES: int = int(os.getenv('DEEP_CRAWL_MAX_PAGES', '10'))
    DEEP_CRAWL_DELAY: float = float(os.getenv('DEEP_CRAWL_DELAY', '1.0'))
    
    # Notification Configuration
    NOTIFICATION_WEBHOOK_URL: Optional[str] = os.getenv('NOTIFICATION_WEBHOOK_URL')
    NOTIFICATION_EMAIL: Optional[str] = os.getenv('NOTIFICATION_EMAIL', 'risunsemi@gmail.com')
    
    # Email Configuration
    EMAIL_HOST: str = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT: int = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USE_TLS: bool = os.getenv('EMAIL_USE_TLS', 'true').lower() == 'true'
    EMAIL_USERNAME: str = os.getenv('EMAIL_USERNAME', 'risunsemi@gmail.com')
    EMAIL_PASSWORD: str = os.getenv('EMAIL_PASSWORD', '')
    
    # System Configuration
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', '3'))
    BATCH_SIZE: int = int(os.getenv('BATCH_SIZE', '10'))
    DEBUG_MODE: bool = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    
    # Multi-site scraping configuration
    ENABLE_MULTI_SITE: bool = os.getenv('ENABLE_MULTI_SITE', 'true').lower() == 'true'
    MAX_TOTAL_ITEMS: int = int(os.getenv('MAX_TOTAL_ITEMS', '500'))  # 增加总数限制
    
    @classmethod
    def get_enabled_sites(cls) -> List[str]:
        """Get list of enabled sites for scraping"""
        enabled_sites = []
        for site, config in cls.SITE_CONFIGS.items():
            if config.get('enabled', True):
                enabled_sites.append(site)
        return enabled_sites
    
    @classmethod
    def get_site_config(cls, site_domain: str) -> dict:
        """Get configuration for a specific site"""
        for site, config in cls.SITE_CONFIGS.items():
            if site in site_domain:
                return config
        return {
            'enabled': True,
            'max_items': 30,
            'delay': 2,
            'use_selenium': True
        }
    
    @classmethod
    def get_crawl4ai_config(cls) -> dict:
        """Get Crawl4AI configuration"""
        return {
            'use_crawl4ai': cls.USE_CRAWL4AI,
            'headless': cls.CRAWL4AI_HEADLESS,
            'verbose': cls.CRAWL4AI_VERBOSE,
            'cache_mode': cls.CRAWL4AI_CACHE_MODE,
            'max_concurrent': cls.CRAWL4AI_MAX_CONCURRENT,
            'browser_type': cls.CRAWL4AI_BROWSER_TYPE,
            'user_agent': cls.CRAWL4AI_USER_AGENT,
            'viewport': {
                'width': cls.CRAWL4AI_VIEWPORT_WIDTH,
                'height': cls.CRAWL4AI_VIEWPORT_HEIGHT
            },
            'wait_timeout': cls.CRAWL4AI_WAIT_TIMEOUT,
            'enable_screenshots': cls.CRAWL4AI_ENABLE_SCREENSHOTS,
            'enable_network_capture': cls.CRAWL4AI_ENABLE_NETWORK_CAPTURE,
        }
    
    @classmethod
    def get_llm_config(cls) -> dict:
        """Get LLM configuration"""
        return {
            'enable_llm_extraction': cls.ENABLE_LLM_EXTRACTION,
            'provider': cls.LLM_PROVIDER,
            'api_token': cls.OPENAI_API_KEY,
            'max_tokens': cls.LLM_MAX_TOKENS,
            'temperature': cls.LLM_TEMPERATURE,
        }
    
    @classmethod
    def get_content_filter_config(cls) -> dict:
        """Get content filter configuration"""
        return {
            'filter_type': cls.CONTENT_FILTER_TYPE,
            'threshold': cls.CONTENT_FILTER_THRESHOLD,
            'min_words': cls.CONTENT_FILTER_MIN_WORDS,
            'bm25_query': cls.BM25_QUERY,
            'bm25_threshold': cls.BM25_THRESHOLD,
        }
    
    @classmethod
    def get_deep_crawl_config(cls) -> dict:
        """Get deep crawling configuration"""
        return {
            'enable_deep_crawl': cls.ENABLE_DEEP_CRAWL,
            'strategy': cls.DEEP_CRAWL_STRATEGY,
            'max_depth': cls.DEEP_CRAWL_MAX_DEPTH,
            'max_pages': cls.DEEP_CRAWL_MAX_PAGES,
            'delay': cls.DEEP_CRAWL_DELAY,
        }
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        required_fields = [
            'OPENAI_API_KEY'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not getattr(cls, field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"Missing required configuration fields: {', '.join(missing_fields)}")
            return False
        
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration (hiding sensitive data)"""
        print("Current Configuration:")
        print(f"  TARGET_URL: {cls.TARGET_URL}")
        print(f"  ENABLE_MULTI_SITE: {cls.ENABLE_MULTI_SITE}")
        print(f"  TARGET_URLS: {len(cls.TARGET_URLS)} sites configured")
        for i, url in enumerate(cls.TARGET_URLS, 1):
            print(f"    {i}. {url}")
        print(f"  SCRAPING_DELAY: {cls.SCRAPING_DELAY}")
        print(f"  MAX_RETRIES: {cls.MAX_RETRIES}")
        print(f"  BATCH_SIZE: {cls.BATCH_SIZE}")
        print(f"  DEBUG_MODE: {cls.DEBUG_MODE}")
        print(f"  MAX_TOTAL_ITEMS: {cls.MAX_TOTAL_ITEMS}")
        print(f"  OPENAI_API_KEY: {'*' * 20 if cls.OPENAI_API_KEY else 'Not set'}")
        print(f"  NOTIFICATION_EMAIL: {cls.NOTIFICATION_EMAIL}")
        print(f"  EMAIL_HOST: {cls.EMAIL_HOST}")
        print(f"  EMAIL_PORT: {cls.EMAIL_PORT}")
        print(f"  EMAIL_PASSWORD: {'*' * 16 if cls.EMAIL_PASSWORD else 'Not set'}")
        print("  GOOGLE_SHEETS: ❌ Removed - Using backup outputs only")
        print("  ENABLED_SITES:")
        for site in cls.get_enabled_sites():
            print(f"    - {site}")
        
        # Print Crawl4AI configuration
        print("\n  CRAWL4AI Configuration:")
        print(f"    USE_CRAWL4AI: {cls.USE_CRAWL4AI}")
        print(f"    HEADLESS: {cls.CRAWL4AI_HEADLESS}")
        print(f"    VERBOSE: {cls.CRAWL4AI_VERBOSE}")
        print(f"    CACHE_MODE: {cls.CRAWL4AI_CACHE_MODE}")
        print(f"    MAX_CONCURRENT: {cls.CRAWL4AI_MAX_CONCURRENT}")
        print(f"    BROWSER_TYPE: {cls.CRAWL4AI_BROWSER_TYPE}")
        print(f"    VIEWPORT: {cls.CRAWL4AI_VIEWPORT_WIDTH}x{cls.CRAWL4AI_VIEWPORT_HEIGHT}")
        print(f"    WAIT_TIMEOUT: {cls.CRAWL4AI_WAIT_TIMEOUT}ms")
        print(f"    ENABLE_SCREENSHOTS: {cls.CRAWL4AI_ENABLE_SCREENSHOTS}")
        print(f"    ENABLE_NETWORK_CAPTURE: {cls.CRAWL4AI_ENABLE_NETWORK_CAPTURE}")
        
        # Print LLM configuration
        print("\n  LLM Configuration:")
        print(f"    ENABLE_LLM_EXTRACTION: {cls.ENABLE_LLM_EXTRACTION}")
        print(f"    LLM_PROVIDER: {cls.LLM_PROVIDER}")
        print(f"    LLM_MAX_TOKENS: {cls.LLM_MAX_TOKENS}")
        print(f"    LLM_TEMPERATURE: {cls.LLM_TEMPERATURE}")
        
        # Print Content Filter configuration
        print("\n  Content Filter Configuration:")
        print(f"    FILTER_TYPE: {cls.CONTENT_FILTER_TYPE}")
        print(f"    THRESHOLD: {cls.CONTENT_FILTER_THRESHOLD}")
        print(f"    MIN_WORDS: {cls.CONTENT_FILTER_MIN_WORDS}")
        print(f"    BM25_QUERY: {cls.BM25_QUERY}")
        print(f"    BM25_THRESHOLD: {cls.BM25_THRESHOLD}")
        
        # Print Deep Crawl configuration
        print("\n  Deep Crawl Configuration:")
        print(f"    ENABLE_DEEP_CRAWL: {cls.ENABLE_DEEP_CRAWL}")
        print(f"    STRATEGY: {cls.DEEP_CRAWL_STRATEGY}")
        print(f"    MAX_DEPTH: {cls.DEEP_CRAWL_MAX_DEPTH}")
        print(f"    MAX_PAGES: {cls.DEEP_CRAWL_MAX_PAGES}")
        print(f"    DELAY: {cls.DEEP_CRAWL_DELAY}s") 