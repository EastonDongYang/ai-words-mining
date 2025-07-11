import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the AI Words Mining System"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    
    # Google Sheets Configuration (removed - using backup outputs only)
    
    # Scraping Configuration
    TARGET_URL: str = os.getenv('TARGET_URL', 'https://www.toolify.ai/new')
    SCRAPING_DELAY: int = int(os.getenv('SCRAPING_DELAY', '2'))
    
    # Notification Configuration
    NOTIFICATION_WEBHOOK_URL: Optional[str] = os.getenv('NOTIFICATION_WEBHOOK_URL')
    NOTIFICATION_EMAIL: Optional[str] = os.getenv('NOTIFICATION_EMAIL', 'risunsemi@gmail.com')
    
    # System Configuration
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', '3'))
    BATCH_SIZE: int = int(os.getenv('BATCH_SIZE', '10'))
    DEBUG_MODE: bool = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    
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
        print(f"  SCRAPING_DELAY: {cls.SCRAPING_DELAY}")
        print(f"  MAX_RETRIES: {cls.MAX_RETRIES}")
        print(f"  BATCH_SIZE: {cls.BATCH_SIZE}")
        print(f"  DEBUG_MODE: {cls.DEBUG_MODE}")
        print(f"  OPENAI_API_KEY: {'*' * 20 if cls.OPENAI_API_KEY else 'Not set'}")
        print(f"  NOTIFICATION_EMAIL: {cls.NOTIFICATION_EMAIL}")
        print("  GOOGLE_SHEETS: ❌ Removed - Using backup outputs only") 