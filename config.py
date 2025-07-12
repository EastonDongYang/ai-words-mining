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
            'max_items': 50,
            'delay': 2,
            'use_selenium': True
        },
        'producthunt.com': {
            'enabled': True,
            'max_items': 30,
            'delay': 3,
            'use_selenium': True
        },
        'futuretools.io': {
            'enabled': True,
            'max_items': 40,
            'delay': 2,
            'use_selenium': True
        },
        'betalist.com': {
            'enabled': True,
            'max_items': 25,
            'delay': 2,
            'use_selenium': False
        },
        'explodingtopics.com': {
            'enabled': True,
            'max_items': 20,
            'delay': 3,
            'use_selenium': True
        }
    }
    
    SCRAPING_DELAY: int = int(os.getenv('SCRAPING_DELAY', '2'))
    
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
    MAX_TOTAL_ITEMS: int = int(os.getenv('MAX_TOTAL_ITEMS', '200'))
    
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