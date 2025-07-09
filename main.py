#!/usr/bin/env python3
"""
AI Words Mining System - Main Workflow
GitHub Actions + OpenAI API + Google Sheets = Zero-maintenance AI New Words Mining System
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import Config
from src.web_scraper import AIToolsScraper
from src.openai_analyzer import OpenAIAnalyzer
from src.data_processor import DataProcessor
from src.google_sheets_integration import GoogleSheetsIntegration
from src.notification_system import NotificationSystem

class AIWordsMiningSystem:
    """Main AI Words Mining System orchestrator"""
    
    def __init__(self):
        self.config = Config()
        self.scraper = AIToolsScraper()
        self.analyzer = OpenAIAnalyzer()
        self.processor = DataProcessor()
        self.sheets_integration = GoogleSheetsIntegration()
        self.notification_system = NotificationSystem()
        self.start_time = datetime.now()
        
        # Statistics tracking
        self.stats = {
            'scraped_tools': 0,
            'extracted_words': 0,
            'processed_words': 0,
            'sheets_updated': False,
            'notifications_sent': False,
            'errors': [],
            'warnings': []
        }
    
    def validate_configuration(self) -> bool:
        """Validate system configuration"""
        print("🔍 Validating configuration...")
        
        if not self.config.validate():
            print("❌ Configuration validation failed")
            return False
        
        print("✅ Configuration validation passed")
        
        # Print configuration summary
        if self.config.DEBUG_MODE:
            self.config.print_config()
        
        return True
    
    def test_integrations(self) -> bool:
        """Test all system integrations"""
        print("🔧 Testing system integrations...")
        
        success = True
        
        # Test OpenAI API
        try:
            print("  - Testing OpenAI API...")
            test_tools = [{"name": "Test Tool", "description": "Test description", "categories": ["Test"]}]
            test_result = self.analyzer.analyze_tools_batch(test_tools)
            if test_result:
                print("  ✅ OpenAI API connection successful")
            else:
                print("  ⚠️ OpenAI API test returned no results")
        except Exception as e:
            print(f"  ❌ OpenAI API test failed: {e}")
            success = False
        
        # Test Google Sheets
        try:
            print("  - Testing Google Sheets API...")
            if self.sheets_integration.test_connection():
                print("  ✅ Google Sheets connection successful")
            else:
                print("  ❌ Google Sheets connection failed")
                success = False
        except Exception as e:
            print(f"  ❌ Google Sheets test failed: {e}")
            success = False
        
        # Test Notifications
        try:
            print("  - Testing notification system...")
            # Only test if webhook is configured
            if self.config.NOTIFICATION_WEBHOOK_URL:
                if self.notification_system.test_notifications():
                    print("  ✅ Notification system working")
                else:
                    print("  ⚠️ Notification system test failed")
            else:
                print("  ⚠️ No notification webhook configured")
        except Exception as e:
            print(f"  ❌ Notification test failed: {e}")
        
        return success
    
    def scrape_ai_tools(self) -> List[Dict]:
        """Scrape AI tools from the target website"""
        print("🕷️ Scraping AI tools...")
        
        try:
            # Send start notification
            self.notification_system.notify_start(self.config.TARGET_URL)
            
            # Scrape tools
            tools_data = self.scraper.scrape(self.config.TARGET_URL)
            
            if not tools_data:
                print("❌ 主爬虫没有获取到数据，尝试使用模拟数据...")
                from src.mock_web_scraper import MockWebScraper
                mock_scraper = MockWebScraper()
                tools_data = mock_scraper.scrape_ai_tools()
                
                if not tools_data:
                    raise Exception("No tools data scraped (including mock data)")
                    
                self.stats['warnings'].append("Used mock data due to scraping failure")
            
            self.stats['scraped_tools'] = len(tools_data)
            print(f"✅ Successfully obtained {len(tools_data)} AI tools")
            
            # Save scraped data for debugging
            if self.config.DEBUG_MODE:
                self.scraper.save_to_json(tools_data, "debug_scraped_tools.json")
            
            return tools_data
            
        except Exception as e:
            error_msg = f"Failed to scrape AI tools: {str(e)}"
            print(f"❌ {error_msg}")
            self.stats['errors'].append(error_msg)
            raise
    
    def analyze_tools(self, tools_data: List[Dict]) -> List[Dict]:
        """Analyze tools and extract new words using OpenAI"""
        print("🧠 Analyzing tools with OpenAI...")
        
        try:
            # Analyze and extract new words
            extracted_words = self.analyzer.analyze_and_extract(tools_data)
            
            if not extracted_words:
                self.stats['warnings'].append("No new words extracted from analysis")
                print("⚠️ No new words extracted")
                return []
            
            self.stats['extracted_words'] = len(extracted_words)
            print(f"✅ Extracted {len(extracted_words)} new words/terms")
            
            # Save analysis results for debugging
            if self.config.DEBUG_MODE:
                self.analyzer.save_analysis_results(extracted_words, "debug_extracted_words.json")
            
            return extracted_words
            
        except Exception as e:
            error_msg = f"Failed to analyze tools: {str(e)}"
            print(f"❌ {error_msg}")
            self.stats['errors'].append(error_msg)
            raise
    
    def process_words(self, words_data: List[Dict]) -> Dict:
        """Process and deduplicate words"""
        print("⚙️ Processing and deduplicating words...")
        
        try:
            # Process words
            processed_result = self.processor.process_extracted_words(words_data)
            
            processed_words = processed_result.get('words', [])
            summary_stats = processed_result.get('summary', {})
            
            self.stats['processed_words'] = len(processed_words)
            print(f"✅ Processed {len(processed_words)} unique words")
            
            # Export to CSV for easy analysis
            if processed_words:
                self.processor.export_to_csv(processed_words, "ai_words_export.csv")
            
            return processed_result
            
        except Exception as e:
            error_msg = f"Failed to process words: {str(e)}"
            print(f"❌ {error_msg}")
            self.stats['errors'].append(error_msg)
            raise
    
    def update_google_sheets(self, words_data: List[Dict], summary_data: Dict) -> str:
        """Update Google Sheets with processed data"""
        print("📊 Updating Google Sheets...")
        
        try:
            # Update sheets
            success = self.sheets_integration.update_words_and_summary(words_data, summary_data)
            
            if success:
                self.stats['sheets_updated'] = True
                print("✅ Google Sheets updated successfully")
                
                # Get sheet URL
                sheet_info = self.sheets_integration.get_sheet_info()
                if sheet_info:
                    return sheet_info.get('url', '')
                
                return ''
            else:
                raise Exception("Failed to update Google Sheets")
                
        except Exception as e:
            error_msg = f"Failed to update Google Sheets: {str(e)}"
            print(f"❌ {error_msg}")
            self.stats['errors'].append(error_msg)
            raise
    
    def send_completion_notification(self, words_data: List[Dict], summary_data: Dict, sheets_url: str = None):
        """Send completion notification"""
        print("📬 Sending completion notification...")
        
        try:
            # Determine notification type based on results
            if self.stats['errors']:
                # Send error notification
                error_msg = "; ".join(self.stats['errors'])
                self.notification_system.notify_error(
                    error_msg, 
                    "Processing", 
                    {
                        'scraped_count': self.stats['scraped_tools'],
                        'processed_count': self.stats['processed_words']
                    }
                )
            elif self.stats['warnings']:
                # Send warning notification
                self.notification_system.notify_warning(self.stats['warnings'], summary_data)
            else:
                # Send success notification
                self.notification_system.notify_success(
                    words_data, 
                    summary_data, 
                    sheets_url, 
                    self.config.TARGET_URL
                )
            
            self.stats['notifications_sent'] = True
            print("✅ Notification sent successfully")
            
        except Exception as e:
            error_msg = f"Failed to send notification: {str(e)}"
            print(f"❌ {error_msg}")
            self.stats['warnings'].append(error_msg)
    
    def print_execution_summary(self):
        """Print execution summary"""
        end_time = datetime.now()
        execution_time = end_time - self.start_time
        
        print("\n" + "="*60)
        print("📋 EXECUTION SUMMARY")
        print("="*60)
        print(f"⏰ Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏰ End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏱️ Execution time: {execution_time}")
        print(f"🕷️ Tools scraped: {self.stats['scraped_tools']}")
        print(f"🧠 Words extracted: {self.stats['extracted_words']}")
        print(f"⚙️ Words processed: {self.stats['processed_words']}")
        print(f"📊 Sheets updated: {'✅' if self.stats['sheets_updated'] else '❌'}")
        print(f"📬 Notifications sent: {'✅' if self.stats['notifications_sent'] else '❌'}")
        
        if self.stats['errors']:
            print(f"❌ Errors: {len(self.stats['errors'])}")
            for error in self.stats['errors']:
                print(f"   - {error}")
        
        if self.stats['warnings']:
            print(f"⚠️ Warnings: {len(self.stats['warnings'])}")
            for warning in self.stats['warnings']:
                print(f"   - {warning}")
        
        print("="*60)
    
    def run(self) -> bool:
        """Main execution method"""
        print("🚀 Starting AI Words Mining System...")
        print(f"📅 Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Step 1: Validate configuration
            if not self.validate_configuration():
                return False
            
            # Step 2: Test integrations
            if not self.test_integrations():
                print("⚠️ Some integration tests failed, but continuing...")
            
            # Step 3: Scrape AI tools
            tools_data = self.scrape_ai_tools()
            
            # Step 4: Analyze tools with OpenAI
            extracted_words = self.analyze_tools(tools_data)
            
            # Step 5: Process and deduplicate words
            processed_result = self.process_words(extracted_words)
            
            # Step 6: Update Google Sheets
            sheets_url = self.update_google_sheets(
                processed_result.get('words', []),
                processed_result.get('summary', {})
            )
            
            # Step 7: Send completion notification
            self.send_completion_notification(
                processed_result.get('words', []),
                processed_result.get('summary', {}),
                sheets_url
            )
            
            # Print summary
            self.print_execution_summary()
            
            print("🎉 AI Words Mining System completed successfully!")
            return True
            
        except Exception as e:
            print(f"💥 System failed with error: {str(e)}")
            
            # Try to send error notification
            try:
                self.notification_system.notify_error(
                    str(e), 
                    "System Execution",
                    {
                        'scraped_count': self.stats['scraped_tools'],
                        'processed_count': self.stats['processed_words']
                    }
                )
            except:
                pass
            
            # Print summary even on failure
            self.print_execution_summary()
            
            return False
    
    def run_test_mode(self) -> bool:
        """Run system in test mode with minimal data"""
        print("🧪 Running in test mode...")
        
        # Use sample data for testing
        sample_tools = [
            {
                "name": "GPT-4 Turbo",
                "description": "Advanced large language model with multimodal capabilities and improved reasoning",
                "categories": ["LLM", "Multimodal AI", "Reasoning"]
            },
            {
                "name": "Claude 3 Opus",
                "description": "Constitutional AI assistant with advanced reasoning and safety features",
                "categories": ["LLM", "Constitutional AI", "Safety"]
            },
            {
                "name": "Gemini Ultra",
                "description": "Google's most capable AI model with multimodal understanding",
                "categories": ["LLM", "Multimodal", "Google AI"]
            }
        ]
        
        try:
            # Test analysis
            extracted_words = self.analyzer.analyze_and_extract(sample_tools)
            
            # Test processing
            processed_result = self.processor.process_extracted_words(extracted_words)
            
            # Test sheets update
            sheets_url = self.update_google_sheets(
                processed_result.get('words', []),
                processed_result.get('summary', {})
            )
            
            # Test notification
            self.send_completion_notification(
                processed_result.get('words', []),
                processed_result.get('summary', {}),
                sheets_url
            )
            
            print("✅ Test mode completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Test mode failed: {str(e)}")
            return False

def main():
    """Main entry point"""
    system = AIWordsMiningSystem()
    
    # Check if running in test mode
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        success = system.run_test_mode()
    else:
        success = system.run()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 