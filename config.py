import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the AI Words Mining System"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    
    # Google Sheets Configuration
    GOOGLE_SHEETS_CREDENTIALS_PATH: str = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH', 'credentials.json')
    GOOGLE_SHEETS_ID: str = os.getenv('GOOGLE_SHEETS_ID', '')
    GOOGLE_SHEETS_RANGE: str = os.getenv('GOOGLE_SHEETS_RANGE', 'Sheet1!A:Z')
    
    # Scraping Configuration
    TARGET_URL: str = os.getenv('TARGET_URL', 'https://theresanaiforthat.com/trending/week/top-50/?pos=1')
    SCRAPING_DELAY: int = int(os.getenv('SCRAPING_DELAY', '2'))
    
    # Notification Configuration
    NOTIFICATION_WEBHOOK_URL: Optional[str] = os.getenv('NOTIFICATION_WEBHOOK_URL')
    NOTIFICATION_EMAIL: Optional[str] = os.getenv('NOTIFICATION_EMAIL')
    
    # System Configuration
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', '3'))
    BATCH_SIZE: int = int(os.getenv('BATCH_SIZE', '10'))
    DEBUG_MODE: bool = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        required_fields = [
            'OPENAI_API_KEY',
            'GOOGLE_SHEETS_ID'
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
        print(f"  GOOGLE_SHEETS_RANGE: {cls.GOOGLE_SHEETS_RANGE}")
        print(f"  MAX_RETRIES: {cls.MAX_RETRIES}")
        print(f"  BATCH_SIZE: {cls.BATCH_SIZE}")
        print(f"  DEBUG_MODE: {cls.DEBUG_MODE}")
        print(f"  OPENAI_API_KEY: {'*' * 20 if cls.OPENAI_API_KEY else 'Not set'}")
        print(f"  GOOGLE_SHEETS_ID: {'*' * 20 if cls.GOOGLE_SHEETS_ID else 'Not set'}") 