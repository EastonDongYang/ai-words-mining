import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
from datetime import datetime
from config import Config

class NotificationSystem:
    """Notification system for sending completion notifications and status updates"""
    
    def __init__(self):
        self.config = Config()
        
    def send_webhook_notification(self, data: Dict) -> bool:
        """Send notification via webhook (e.g., Slack, Discord, etc.)"""
        if not self.config.NOTIFICATION_WEBHOOK_URL:
            print("No webhook URL configured")
            return False
        
        try:
            # Prepare notification payload
            payload = {
                "text": self.format_notification_text(data),
                "username": "AI Words Mining Bot",
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                self.config.NOTIFICATION_WEBHOOK_URL,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                print("Webhook notification sent successfully")
                return True
            else:
                print(f"Webhook notification failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error sending webhook notification: {e}")
            return False
    
    def send_email_notification(self, data: Dict) -> bool:
        """Send notification via email"""
        if not self.config.NOTIFICATION_EMAIL:
            print("No email configured")
            return False
        
        try:
            # This is a placeholder - you'll need to configure SMTP settings
            # For production, use services like SendGrid, AWS SES, etc.
            print("Email notification would be sent here")
            print(f"To: {self.config.NOTIFICATION_EMAIL}")
            print(f"Subject: AI Words Mining System - Report")
            print(f"Body: {self.format_notification_text(data)}")
            
            return True
            
        except Exception as e:
            print(f"Error sending email notification: {e}")
            return False
    
    def format_notification_text(self, data: Dict) -> str:
        """Format notification text based on data"""
        status = data.get('status', 'unknown')
        
        if status == 'success':
            return self.format_success_notification(data)
        elif status == 'error':
            return self.format_error_notification(data)
        elif status == 'warning':
            return self.format_warning_notification(data)
        else:
            return self.format_general_notification(data)
    
    def format_success_notification(self, data: Dict) -> str:
        """Format successful completion notification"""
        message = "🎉 AI Words Mining System - Success Report\n\n"
        
        # Add timestamp
        message += f"⏰ Completed: {data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n\n"
        
        # Add summary statistics
        summary = data.get('summary', {})
        if summary:
            message += "📊 Summary:\n"
            message += f"• Total Words Extracted: {summary.get('total_words', 0)}\n"
            message += f"• Emerging Terms: {summary.get('emerging_terms_count', 0)}\n"
            message += f"• Average Trend Score: {summary.get('average_trend_score', 0)}\n"
            message += f"• Categories: {len(summary.get('categories', {}))}\n\n"
        
        # Add top categories
        if summary.get('top_categories'):
            message += "🏆 Top Categories:\n"
            for category, count in summary.get('top_categories', [])[:5]:
                message += f"• {category}: {count} words\n"
            message += "\n"
        
        # Add top words
        words = data.get('words', [])
        if words:
            message += "🔥 Top 5 Words:\n"
            for i, word in enumerate(words[:5], 1):
                message += f"{i}. {word.get('word', 'Unknown')} ({word.get('category', 'Unknown')})\n"
            message += "\n"
        
        # Add Google Sheets link
        sheets_url = data.get('sheets_url')
        if sheets_url:
            message += f"📋 View Full Report: {sheets_url}\n\n"
        
        # Add source information
        message += f"📄 Source: {data.get('source_url', 'Unknown')}\n"
        message += f"🔄 Next run: {data.get('next_run', 'Scheduled')}\n"
        
        return message
    
    def format_error_notification(self, data: Dict) -> str:
        """Format error notification"""
        message = "❌ AI Words Mining System - Error Report\n\n"
        
        # Add timestamp
        message += f"⏰ Time: {data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n\n"
        
        # Add error details
        error = data.get('error', 'Unknown error')
        message += f"🚨 Error: {error}\n\n"
        
        # Add stage where error occurred
        stage = data.get('stage', 'Unknown stage')
        message += f"📍 Stage: {stage}\n\n"
        
        # Add any partial results
        if data.get('partial_results'):
            message += "⚠️ Partial Results Available:\n"
            partial = data.get('partial_results', {})
            if partial.get('scraped_count'):
                message += f"• Scraped: {partial['scraped_count']} tools\n"
            if partial.get('processed_count'):
                message += f"• Processed: {partial['processed_count']} words\n"
            message += "\n"
        
        # Add next steps
        message += "🔧 Next Steps:\n"
        message += "• Check system logs\n"
        message += "• Verify API credentials\n"
        message += "• Check network connectivity\n"
        message += "• System will retry on next scheduled run\n"
        
        return message
    
    def format_warning_notification(self, data: Dict) -> str:
        """Format warning notification"""
        message = "⚠️ AI Words Mining System - Warning Report\n\n"
        
        # Add timestamp
        message += f"⏰ Time: {data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n\n"
        
        # Add warning details
        warnings = data.get('warnings', [])
        if warnings:
            message += "⚠️ Warnings:\n"
            for warning in warnings:
                message += f"• {warning}\n"
            message += "\n"
        
        # Add summary if available
        summary = data.get('summary', {})
        if summary:
            message += "📊 Completed with warnings:\n"
            message += f"• Total Words: {summary.get('total_words', 0)}\n"
            message += f"• Emerging Terms: {summary.get('emerging_terms_count', 0)}\n\n"
        
        # Add recommendation
        message += "💡 Recommendations:\n"
        message += "• Review system configuration\n"
        message += "• Check API rate limits\n"
        message += "• Monitor for recurring issues\n"
        
        return message
    
    def format_general_notification(self, data: Dict) -> str:
        """Format general notification"""
        message = "ℹ️ AI Words Mining System - Status Update\n\n"
        
        # Add timestamp
        message += f"⏰ Time: {data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n\n"
        
        # Add message
        message += f"📝 Status: {data.get('message', 'System update')}\n\n"
        
        # Add any additional data
        if data.get('details'):
            message += "📋 Details:\n"
            for key, value in data.get('details', {}).items():
                message += f"• {key}: {value}\n"
        
        return message
    
    def notify_success(self, words_data: List[Dict], summary_data: Dict, sheets_url: str = None, source_url: str = None) -> bool:
        """Send success notification"""
        notification_data = {
            'status': 'success',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'words': words_data,
            'summary': summary_data,
            'sheets_url': sheets_url,
            'source_url': source_url,
            'next_run': 'Next scheduled run'
        }
        
        success = True
        
        # Send webhook notification
        if not self.send_webhook_notification(notification_data):
            success = False
        
        # Send email notification
        if not self.send_email_notification(notification_data):
            success = False
        
        return success
    
    def notify_error(self, error_message: str, stage: str = None, partial_results: Dict = None) -> bool:
        """Send error notification"""
        notification_data = {
            'status': 'error',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error': error_message,
            'stage': stage or 'Unknown',
            'partial_results': partial_results or {}
        }
        
        success = True
        
        # Send webhook notification
        if not self.send_webhook_notification(notification_data):
            success = False
        
        # Send email notification
        if not self.send_email_notification(notification_data):
            success = False
        
        return success
    
    def notify_warning(self, warnings: List[str], summary_data: Dict = None) -> bool:
        """Send warning notification"""
        notification_data = {
            'status': 'warning',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'warnings': warnings,
            'summary': summary_data or {}
        }
        
        success = True
        
        # Send webhook notification
        if not self.send_webhook_notification(notification_data):
            success = False
        
        # Send email notification
        if not self.send_email_notification(notification_data):
            success = False
        
        return success
    
    def notify_start(self, source_url: str = None) -> bool:
        """Send start notification"""
        notification_data = {
            'status': 'info',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'message': 'AI Words Mining System Started',
            'details': {
                'source_url': source_url or 'Unknown',
                'stage': 'Initialization'
            }
        }
        
        success = True
        
        # Send webhook notification
        if not self.send_webhook_notification(notification_data):
            success = False
        
        return success
    
    def create_slack_payload(self, data: Dict) -> Dict:
        """Create Slack-specific payload"""
        text = self.format_notification_text(data)
        status = data.get('status', 'unknown')
        
        # Choose emoji and color based on status
        if status == 'success':
            color = 'good'
            icon = ':white_check_mark:'
        elif status == 'error':
            color = 'danger'
            icon = ':x:'
        elif status == 'warning':
            color = 'warning'
            icon = ':warning:'
        else:
            color = '#36a64f'
            icon = ':information_source:'
        
        return {
            "username": "AI Words Mining Bot",
            "icon_emoji": icon,
            "attachments": [{
                "color": color,
                "text": text,
                "footer": "AI Words Mining System",
                "ts": int(datetime.now().timestamp())
            }]
        }
    
    def create_discord_payload(self, data: Dict) -> Dict:
        """Create Discord-specific payload"""
        text = self.format_notification_text(data)
        status = data.get('status', 'unknown')
        
        # Choose color based on status
        if status == 'success':
            color = 0x00ff00  # Green
        elif status == 'error':
            color = 0xff0000  # Red
        elif status == 'warning':
            color = 0xffff00  # Yellow
        else:
            color = 0x0099ff  # Blue
        
        return {
            "username": "AI Words Mining Bot",
            "embeds": [{
                "title": "AI Words Mining System Report",
                "description": text,
                "color": color,
                "timestamp": datetime.now().isoformat(),
                "footer": {
                    "text": "AI Words Mining System"
                }
            }]
        }
    
    def test_notifications(self) -> bool:
        """Test notification systems"""
        test_data = {
            'status': 'success',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'summary': {
                'total_words': 42,
                'emerging_terms_count': 15,
                'average_trend_score': 7.5,
                'categories': {'AI Model': 10, 'Technology': 8, 'Methodology': 6}
            },
            'words': [
                {'word': 'Test Word 1', 'category': 'AI Model'},
                {'word': 'Test Word 2', 'category': 'Technology'}
            ],
            'sheets_url': 'https://docs.google.com/spreadsheets/d/test',
            'source_url': 'https://www.toolify.ai/test'
        }
        
        print("Testing notification system...")
        success = self.send_webhook_notification(test_data)
        
        if success:
            print("✓ Notification test passed")
        else:
            print("✗ Notification test failed")
        
        return success

if __name__ == "__main__":
    # Test the notification system
    notification_system = NotificationSystem()
    
    # Test notifications
    notification_system.test_notifications()
    
    # Test different notification types
    print("\nTesting error notification...")
    notification_system.notify_error("Test error message", "Testing Stage")
    
    print("\nTesting warning notification...")
    notification_system.notify_warning(["Test warning 1", "Test warning 2"])
    
    print("\nTesting start notification...")
    notification_system.notify_start("https://test.com") 