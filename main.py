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
from src.toolify_scraper import ToolifyScraper
from src.multi_site_scraper import MultiSiteScraper
from src.openai_analyzer import OpenAIAnalyzer
from src.data_processor import DataProcessor
from src.notification_system import NotificationSystem

class AIWordsMiningSystem:
    """Main AI Words Mining System orchestrator"""
    
    def __init__(self):
        self.config = Config()
        self.scraper = ToolifyScraper()  # Keep for backward compatibility
        self.multi_scraper = MultiSiteScraper()  # New multi-site scraper
        self.analyzer = OpenAIAnalyzer()
        self.processor = DataProcessor()
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
        
        # Skip Google Sheets testing (removed)
        print("  - Google Sheets integration removed - using backup outputs only")
        
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
        """Scrape AI tools from multiple websites"""
        print("🕷️ Scraping AI tools from multiple sources...")
        
        try:
            # Send start notification
            if self.config.ENABLE_MULTI_SITE:
                self.notification_system.notify_start("Multiple AI tool websites")
                print(f"🌐 Multi-site scraping enabled - scraping {len(self.config.TARGET_URLS)} sites")
                
                # Use multi-site scraper
                tools_data = self.multi_scraper.scrape_all_sites()
                
                if not tools_data:
                    print("❌ 多网站爬虫没有获取到数据，尝试单网站爬虫...")
                    # Fallback to single site scraper
                    tools_data = self.scraper.scrape(self.config.TARGET_URL)
                    
                    if not tools_data:
                        print("❌ 单网站爬虫也没有获取到数据，尝试使用模拟数据...")
                        from src.mock_web_scraper import MockWebScraper
                        mock_scraper = MockWebScraper()
                        tools_data = mock_scraper.scrape_ai_tools()
                        
                        if not tools_data:
                            raise Exception("No tools data scraped from any source")
                            
                        self.stats['warnings'].append("Used mock data due to all scraping failures")
                    else:
                        self.stats['warnings'].append("Fallback to single site scraper due to multi-site failure")
                else:
                    print(f"✅ Multi-site scraping successful")
                    # Save detailed source statistics
                    source_stats = {}
                    for tool in tools_data:
                        source = tool.get('source', 'unknown')
                        source_stats[source] = source_stats.get(source, 0) + 1
                    
                    print("📊 Source breakdown:")
                    for source, count in source_stats.items():
                        print(f"  - {source}: {count} tools")
                    
                    # Save multi-site scraped data for debugging
                    if self.config.DEBUG_MODE:
                        self.multi_scraper.save_results(tools_data, "debug_multi_site_scraped_tools.json")
            else:
                print("🔗 Single-site scraping mode")
                self.notification_system.notify_start(self.config.TARGET_URL)
                
                # Use single site scraper (original behavior)
                tools_data = self.scraper.scrape(self.config.TARGET_URL)
                
                if not tools_data:
                    print("❌ 单网站爬虫没有获取到数据，尝试使用模拟数据...")
                    from src.mock_web_scraper import MockWebScraper
                    mock_scraper = MockWebScraper()
                    tools_data = mock_scraper.scrape_ai_tools()
                    
                    if not tools_data:
                        raise Exception("No tools data scraped (including mock data)")
                        
                    self.stats['warnings'].append("Used mock data due to scraping failure")
                
                # Save scraped data for debugging
                if self.config.DEBUG_MODE:
                    self.scraper.save_to_json(tools_data, "debug_scraped_tools.json")
            
            self.stats['scraped_tools'] = len(tools_data)
            print(f"✅ Successfully obtained {len(tools_data)} AI tools")
            
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
    
    def create_all_backups(self, words_data: List[Dict], summary_data: Dict) -> str:
        """Create all backup outputs (Google Sheets removed)"""
        print("📄 Creating backup outputs...")
        
        try:
            # Always create backup outputs since Google Sheets is removed
            self.create_backup_outputs(words_data, summary_data)
            self.stats['sheets_updated'] = False  # Google Sheets removed
            print("✅ All backup outputs created successfully")
            return ''
        except Exception as e:
            error_msg = f"Failed to create backup outputs: {str(e)}"
            print(f"❌ {error_msg}")
            self.stats['warnings'].append(error_msg)
            return ''
    
    def create_backup_outputs(self, words_data: List[Dict], summary_data: Dict):
        """Create backup outputs when Google Sheets fails"""
        backup_methods = []
        
        try:
            # 1. Enhanced local file backup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"ai_words_backup_{timestamp}.json"
            
            backup_data = {
                'timestamp': timestamp,
                'summary': summary_data,
                'words': words_data,
                'execution_stats': self.stats,
                'total_words': len(words_data),
                'execution_time': str(datetime.now() - self.start_time)
            }
            
            with open(backup_filename, 'w', encoding='utf-8') as f:
                import json
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Created local backup: {backup_filename}")
            backup_methods.append(f"Local backup: {backup_filename}")
            
            # 2. Email backup (handled by notification_system in send_completion_notification)
            if hasattr(self.config, 'NOTIFICATION_EMAIL') and self.config.NOTIFICATION_EMAIL:
                print("📧 Email notification will be sent via notification system")
                backup_methods.append(f"Email notification configured for: {self.config.NOTIFICATION_EMAIL}")
            
            # 3. GitHub artifact preparation (for CI/CD)
            if self.is_github_actions():
                try:
                    self.prepare_github_artifacts(words_data, summary_data, backup_filename)
                    print("✅ GitHub artifacts prepared")
                    backup_methods.append("GitHub artifacts prepared")
                except Exception as e:
                    print(f"⚠️ GitHub artifacts preparation failed: {e}")
            
            # 4. Create human-readable summary
            self.create_readable_summary(words_data, summary_data, timestamp)
            print("✅ Created readable summary")
            backup_methods.append("Readable summary created")
            
            self.stats['backup_methods'] = backup_methods
            
        except Exception as e:
            print(f"❌ Backup creation failed: {e}")
            self.stats['warnings'].append(f"Backup creation failed: {e}")
    
    def send_email_backup(self, words_data: List[Dict], summary_data: Dict, backup_filename: str):
        """Send email with backup data"""
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        import os
        
        # Email configuration - use the same config as notification system
        smtp_server = self.config.EMAIL_HOST
        smtp_port = self.config.EMAIL_PORT
        sender_email = self.config.EMAIL_USERNAME  # 使用配置的发件人邮箱
        sender_password = self.config.EMAIL_PASSWORD  # 使用配置的应用密码
        receiver_email = self.config.NOTIFICATION_EMAIL or "risunsemi@gmail.com"
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"AI Words Mining Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Email body
        body = f"""
🎉 AI Words Mining System - Results Report

⏰ Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🕷️ Tools Analyzed: {self.stats['scraped_tools']}
🧠 Words Extracted: {self.stats['extracted_words']}
⚙️ Words Processed: {self.stats['processed_words']}
📊 Output Method: ✅ Multiple backup outputs created

📝 Top Extracted Words:
{self.format_words_for_email(words_data[:10])}

📄 Complete data is attached as JSON file.

🔧 System Information:
- Execution Time: {datetime.now() - self.start_time}
- Backup Methods: {', '.join(self.stats.get('backup_methods', []))}
- Target URL: {self.config.TARGET_URL}

Best regards,
AI Words Mining System
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach backup file if exists
        if os.path.exists(backup_filename):
            with open(backup_filename, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {backup_filename}'
                )
                msg.attach(part)
        
        # Send email (注意：这需要邮箱配置，在实际部署中需要设置)
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            # 注意：这里需要邮箱应用密码，不是普通密码
            if sender_password:
                server.login(sender_email, sender_password)
                server.send_message(msg)
                server.quit()
            else:
                print("⚠️ Email password not configured, skipping email send")
        except Exception as e:
            print(f"⚠️ Email send failed: {e}")
            # 创建邮件内容文件作为备用
            with open(f"email_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 'w', encoding='utf-8') as f:
                f.write(body)
            print("✅ Email content saved to local file")
    
    def format_words_for_email(self, words_data: List[Dict]) -> str:
        """Format words data for email display"""
        if not words_data:
            return "No words extracted"
        
        formatted = []
        for i, word in enumerate(words_data, 1):
            formatted.append(f"{i}. {word.get('word', 'N/A')} ({word.get('category', 'N/A')})")
            if word.get('definition'):
                formatted.append(f"   Definition: {word.get('definition', 'N/A')}")
            formatted.append("")  # Empty line
        
        return "\n".join(formatted)
    
    def is_github_actions(self) -> bool:
        """Check if running in GitHub Actions"""
        import os
        return os.getenv('GITHUB_ACTIONS') == 'true'
    
    def prepare_github_artifacts(self, words_data: List[Dict], summary_data: Dict, backup_filename: str):
        """Prepare artifacts for GitHub Actions"""
        import os
        
        # Create artifacts directory
        artifacts_dir = "artifacts"
        os.makedirs(artifacts_dir, exist_ok=True)
        
        # Copy backup file to artifacts
        import shutil
        if os.path.exists(backup_filename):
            shutil.copy2(backup_filename, os.path.join(artifacts_dir, backup_filename))
        
        # Create summary file
        summary_file = os.path.join(artifacts_dir, "execution_summary.md")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"""# AI Words Mining Execution Summary

## 📊 Execution Statistics
- **Start Time**: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
- **End Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Duration**: {datetime.now() - self.start_time}
- **Tools Scraped**: {self.stats['scraped_tools']}
- **Words Extracted**: {self.stats['extracted_words']}
- **Words Processed**: {self.stats['processed_words']}

## 📝 Extracted Words
{self.format_words_for_markdown(words_data)}

## ⚠️ Warnings
{chr(10).join(f"- {warning}" for warning in self.stats.get('warnings', []))}

## 🔧 Backup Methods
{chr(10).join(f"- {method}" for method in self.stats.get('backup_methods', []))}
""")
        
        print(f"✅ GitHub artifacts prepared in {artifacts_dir}/")
    
    def format_words_for_markdown(self, words_data: List[Dict]) -> str:
        """Format words data for markdown display"""
        if not words_data:
            return "No words extracted"
        
        formatted = ["| Word | Category | Definition |", "|------|----------|------------|"]
        for word in words_data:
            formatted.append(f"| {word.get('word', 'N/A')} | {word.get('category', 'N/A')} | {word.get('definition', 'N/A')} |")
        
        return "\n".join(formatted)
    
    def create_readable_summary(self, words_data: List[Dict], summary_data: Dict, timestamp: str):
        """Create a human-readable summary file"""
        summary_filename = f"ai_words_summary_{timestamp}.txt"
        
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write("🎉 AI Words Mining System - Execution Summary\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"📅 Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"⏱️ Duration: {datetime.now() - self.start_time}\n")
            f.write(f"🌐 Target URL: {self.config.TARGET_URL}\n\n")
            
            f.write("📊 Statistics:\n")
            f.write(f"  - Tools Scraped: {self.stats['scraped_tools']}\n")
            f.write(f"  - Words Extracted: {self.stats['extracted_words']}\n")
            f.write(f"  - Words Processed: {self.stats['processed_words']}\n")
            f.write(f"  - Backup Outputs Created: {'✅' if self.stats.get('backup_methods') else '❌'}\n\n")
            
            f.write("📝 Extracted Words:\n")
            f.write("-" * 30 + "\n")
            for i, word in enumerate(words_data, 1):
                f.write(f"{i}. {word.get('word', 'N/A')}\n")
                f.write(f"   Category: {word.get('category', 'N/A')}\n")
                f.write(f"   Definition: {word.get('definition', 'N/A')}\n")
                f.write(f"   Context: {word.get('context', 'N/A')}\n")
                f.write(f"   Importance: {word.get('importance', 'N/A')}\n\n")
            
            if self.stats.get('warnings'):
                f.write("⚠️ Warnings:\n")
                f.write("-" * 30 + "\n")
                for warning in self.stats['warnings']:
                    f.write(f"  - {warning}\n")
                f.write("\n")
            
            f.write("🔧 Backup Methods Used:\n")
            f.write("-" * 30 + "\n")
            for method in self.stats.get('backup_methods', []):
                f.write(f"  - {method}\n")
        
        print(f"✅ Created readable summary: {summary_filename}")
    
    def send_completion_notification(self, words_data: List[Dict], summary_data: Dict, sheets_url: str = None):
        """Send completion notification"""
        print("📬 Sending completion notification...")
        
        try:
            # Prepare attachment files
            attachment_files = []
            
            # Add CSV file if it exists
            csv_file = "ai_words_export.csv"
            if os.path.exists(csv_file):
                attachment_files.append(csv_file)
                print(f"📎 Will attach CSV file: {csv_file}")
            
            # Add backup JSON file if it exists
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            json_files = [f for f in os.listdir('.') if f.startswith('ai_words_backup_') and f.endswith('.json')]
            if json_files:
                # Use the most recent backup file
                latest_backup = max(json_files, key=lambda f: os.path.getmtime(f))
                attachment_files.append(latest_backup)
                print(f"📎 Will attach backup file: {latest_backup}")
            
            # Determine notification type based on results
            if self.stats['errors']:
                # Send error notification with attachments
                error_msg = "; ".join(self.stats['errors'])
                self.notification_system.notify_error(
                    error_msg, 
                    "Processing", 
                    {
                        'scraped_count': self.stats['scraped_tools'],
                        'processed_count': self.stats['processed_words']
                    },
                    attachment_files
                )
            elif self.stats['warnings']:
                # Send warning notification with attachments
                self.notification_system.notify_warning(self.stats['warnings'], summary_data, attachment_files)
            else:
                # Send success notification with attachments
                self.notification_system.notify_success(
                    words_data, 
                    summary_data, 
                    sheets_url, 
                    self.config.TARGET_URL,
                    attachment_files
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
            
            # Step 6: Create backup outputs (Google Sheets removed)
            sheets_url = self.create_all_backups(
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
            
            # Test backup outputs
            sheets_url = self.create_all_backups(
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