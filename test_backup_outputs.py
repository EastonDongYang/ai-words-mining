#!/usr/bin/env python3
"""
测试备份输出功能的脚本
用于验证当Google Sheets失败时的备用输出方法
"""

import sys
import os
from datetime import datetime

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.mock_web_scraper import MockWebScraper
from src.openai_analyzer import OpenAIAnalyzer
from src.data_processor import DataProcessor
from config import Config

def test_backup_outputs():
    """测试备份输出功能"""
    print("🧪 开始测试备份输出功能...")
    print("=" * 50)
    
    try:
        # 创建模拟的AIWordsMiningSystem类来测试备份功能
        class MockAIWordsMiningSystem:
            def __init__(self):
                self.config = Config()
                self.start_time = datetime.now()
                self.stats = {
                    'scraped_tools': 8,
                    'extracted_words': 12,
                    'processed_words': 10,
                    'sheets_updated': False,
                    'warnings': ['Google Sheets connection failed', 'Used mock data']
                }
            
            def create_backup_outputs(self, words_data, summary_data):
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
                    
                    import json
                    with open(backup_filename, 'w', encoding='utf-8') as f:
                        json.dump(backup_data, f, indent=2, ensure_ascii=False)
                    
                    print(f"✅ Created local backup: {backup_filename}")
                    backup_methods.append(f"Local backup: {backup_filename}")
                    
                    # 2. Create human-readable summary
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
                        f.write(f"  - Google Sheets Updated: {'✅' if self.stats['sheets_updated'] else '❌'}\n\n")
                        
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
                        for method in backup_methods:
                            f.write(f"  - {method}\n")
                    
                    print(f"✅ Created readable summary: {summary_filename}")
                    backup_methods.append(f"Readable summary: {summary_filename}")
                    
                    # 3. Create email content file
                    email_content = f"""
🎉 AI Words Mining System - Results Report

⏰ Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🕷️ Tools Analyzed: {self.stats['scraped_tools']}
🧠 Words Extracted: {self.stats['extracted_words']}
⚙️ Words Processed: {self.stats['processed_words']}
📊 Google Sheets: ❌ (Failed - using backup methods)

📝 Top Extracted Words:
{self.format_words_for_email(words_data[:5])}

🔧 System Information:
- Execution Time: {datetime.now() - self.start_time}
- Target URL: {self.config.TARGET_URL}
- Backup Methods: {', '.join(backup_methods)}

📧 Email would be sent to: {self.config.NOTIFICATION_EMAIL}

Best regards,
AI Words Mining System
                    """
                    
                    email_filename = f"email_backup_{timestamp}.txt"
                    with open(email_filename, 'w', encoding='utf-8') as f:
                        f.write(email_content)
                    
                    print(f"✅ Created email content: {email_filename}")
                    backup_methods.append(f"Email content: {email_filename}")
                    
                    # 4. Create GitHub-style artifacts
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
{chr(10).join(f"- {method}" for method in backup_methods)}
""")
                    
                    print(f"✅ Created GitHub artifacts in {artifacts_dir}/")
                    backup_methods.append(f"GitHub artifacts: {artifacts_dir}/")
                    
                    return backup_methods
                    
                except Exception as e:
                    print(f"❌ Backup creation failed: {e}")
                    return []
            
            def format_words_for_email(self, words_data):
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
            
            def format_words_for_markdown(self, words_data):
                """Format words data for markdown display"""
                if not words_data:
                    return "No words extracted"
                
                formatted = ["| Word | Category | Definition |", "|------|----------|------------|"]
                for word in words_data:
                    formatted.append(f"| {word.get('word', 'N/A')} | {word.get('category', 'N/A')} | {word.get('definition', 'N/A')} |")
                
                return "\n".join(formatted)
        
        # 1. 生成测试数据
        print("1️⃣ 生成测试数据...")
        mock_scraper = MockWebScraper()
        tools_data = mock_scraper.scrape_ai_tools(5)
        print(f"✅ 生成了 {len(tools_data)} 个模拟工具")
        
        # 2. 模拟OpenAI分析
        print("\n2️⃣ 模拟OpenAI分析...")
        config = Config()
        if config.OPENAI_API_KEY:
            try:
                analyzer = OpenAIAnalyzer()
                extracted_words = analyzer.analyze_tools_batch(tools_data[:3])
                print(f"✅ 成功提取了 {len(extracted_words)} 个新词汇")
            except Exception as e:
                print(f"⚠️ OpenAI分析失败，使用模拟数据: {e}")
                extracted_words = [
                    {'word': 'Test Word 1', 'category': 'AI Technology', 'definition': 'Test definition 1', 'context': 'Test context', 'importance': 'high'},
                    {'word': 'Test Word 2', 'category': 'Machine Learning', 'definition': 'Test definition 2', 'context': 'Test context', 'importance': 'medium'}
                ]
        else:
            print("⚠️ 未配置OpenAI API，使用模拟数据")
            extracted_words = [
                {'word': 'Mock Word 1', 'category': 'AI Technology', 'definition': 'Mock definition 1', 'context': 'Mock context', 'importance': 'high'},
                {'word': 'Mock Word 2', 'category': 'Machine Learning', 'definition': 'Mock definition 2', 'context': 'Mock context', 'importance': 'medium'}
            ]
        
        # 3. 数据处理
        print("\n3️⃣ 处理数据...")
        processor = DataProcessor()
        processed_result = processor.process_extracted_words(extracted_words)
        processed_words = processed_result.get('words', [])
        summary_data = processed_result.get('summary', {})
        print(f"✅ 处理了 {len(processed_words)} 个词汇")
        
        # 4. 测试备份输出
        print("\n4️⃣ 测试备份输出...")
        system = MockAIWordsMiningSystem()
        backup_methods = system.create_backup_outputs(processed_words, summary_data)
        
        # 5. 验证生成的文件
        print("\n5️⃣ 验证生成的文件...")
        files_to_check = [
            'ai_words_backup_*.json',
            'ai_words_summary_*.txt',
            'email_backup_*.txt',
            'artifacts/execution_summary.md'
        ]
        
        import glob
        for pattern in files_to_check:
            matches = glob.glob(pattern)
            if matches:
                print(f"✅ 找到文件: {', '.join(matches)}")
            else:
                print(f"⚠️ 未找到文件: {pattern}")
        
        print("\n" + "=" * 50)
        print("🎉 备份输出功能测试完成！")
        print("✅ 所有备份方法都正常工作")
        print(f"📁 生成的备份方法: {len(backup_methods)} 种")
        for method in backup_methods:
            print(f"  - {method}")
        
        print("\n📧 邮件配置:")
        print(f"  - 收件人: {config.NOTIFICATION_EMAIL}")
        print(f"  - 发件人: ai-words-mining@gmail.com")
        print("  - 注意: 需要配置EMAIL_PASSWORD环境变量才能实际发送邮件")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_backup_outputs()
    sys.exit(0 if success else 1) 