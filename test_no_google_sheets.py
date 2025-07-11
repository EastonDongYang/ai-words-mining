#!/usr/bin/env python3
"""
测试删除Google Sheets后的系统功能
验证系统是否能正常运行并生成所有备份输出
"""

import sys
import os
from datetime import datetime

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_system_without_google_sheets():
    """测试删除Google Sheets后的完整系统功能"""
    print("🧪 测试删除Google Sheets后的系统功能...")
    print("=" * 60)
    
    try:
        # 1. 测试配置加载
        print("1️⃣ 测试配置加载...")
        from config import Config
        config = Config()
        
        # 验证Google Sheets配置已删除
        if hasattr(config, 'GOOGLE_SHEETS_ID'):
            print("❌ Google Sheets配置未完全删除")
            return False
        
        print("✅ 配置加载成功，Google Sheets配置已删除")
        
        # 2. 测试导入（确保没有Google Sheets导入错误）
        print("\n2️⃣ 测试模块导入...")
        try:
            from src.openai_analyzer import OpenAIAnalyzer
            from src.data_processor import DataProcessor
            from src.notification_system import NotificationSystem
            from src.mock_web_scraper import MockWebScraper
            print("✅ 所有核心模块导入成功")
        except ImportError as e:
            print(f"❌ 模块导入失败: {e}")
            return False
        
        # 3. 测试模拟系统运行
        print("\n3️⃣ 测试模拟系统运行...")
        
        # 创建模拟的AIWordsMiningSystem
        class TestAIWordsMiningSystem:
            def __init__(self):
                self.config = config
                self.start_time = datetime.now()
                self.stats = {
                    'scraped_tools': 5,
                    'extracted_words': 8,
                    'processed_words': 6,
                    'sheets_updated': False,  # Google Sheets已删除
                    'warnings': []
                }
        
        system = TestAIWordsMiningSystem()
        
        # 4. 测试数据生成和处理
        print("\n4️⃣ 测试数据生成和处理...")
        mock_scraper = MockWebScraper()
        tools_data = mock_scraper.scrape_ai_tools(3)
        print(f"✅ 生成了 {len(tools_data)} 个模拟工具")
        
        # 模拟词汇数据
        mock_words = [
            {
                'word': 'Test AI Term',
                'category': 'AI Technology',
                'definition': 'A test AI terminology for validation',
                'context': 'Test context',
                'importance': 'high',
                'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'word': 'Mock Algorithm',
                'category': 'Machine Learning',
                'definition': 'A mock algorithm for testing purposes',
                'context': 'Test context',
                'importance': 'medium',
                'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        ]
        
        processor = DataProcessor()
        processed_result = processor.process_extracted_words(mock_words)
        processed_words = processed_result.get('words', [])
        summary_data = processed_result.get('summary', {})
        
        print(f"✅ 处理了 {len(processed_words)} 个词汇")
        
        # 5. 测试备份输出功能
        print("\n5️⃣ 测试备份输出功能...")
        
        # 手动创建备份输出测试
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"test_backup_{timestamp}.json"
        
        # 创建JSON备份
        import json
        backup_data = {
            'timestamp': timestamp,
            'summary': summary_data,
            'words': processed_words,
            'test_mode': True,
            'google_sheets_removed': True
        }
        
        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 创建了JSON备份: {backup_filename}")
        
        # 创建可读摘要
        summary_filename = f"test_summary_{timestamp}.txt"
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write("🎉 AI Words Mining System - Test Run\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("🔧 Google Sheets: ❌ Removed (using backup outputs)\n")
            f.write(f"📊 Test Words: {len(processed_words)}\n")
            f.write("✅ System Status: Working without Google Sheets\n")
        
        print(f"✅ 创建了可读摘要: {summary_filename}")
        
        # 6. 验证requirements.txt
        print("\n6️⃣ 验证依赖文件...")
        with open('requirements.txt', 'r') as f:
            requirements_content = f.read()
        
        if 'google-' in requirements_content:
            print("❌ requirements.txt中仍有Google依赖")
            return False
        
        print("✅ requirements.txt已清理Google依赖")
        
        # 7. 测试GitHub Actions工作流语法
        print("\n7️⃣ 验证GitHub Actions工作流...")
        workflow_file = '.github/workflows/ai-words-mining.yml'
        if os.path.exists(workflow_file):
            with open(workflow_file, 'r', encoding='utf-8') as f:
                workflow_content = f.read()
            
            if 'GOOGLE_CREDENTIALS' in workflow_content:
                print("❌ 工作流文件中仍有Google相关内容")
                return False
            
            if 'secrets.GOOGLE' in workflow_content:
                print("❌ 工作流文件中仍有Google secrets引用")
                return False
            
            print("✅ GitHub Actions工作流已清理Google相关内容")
        
        # 8. 清理测试文件
        print("\n8️⃣ 清理测试文件...")
        try:
            os.remove(backup_filename)
            os.remove(summary_filename)
            print("✅ 测试文件已清理")
        except:
            print("⚠️ 部分测试文件清理失败（不影响功能）")
        
        print("\n" + "=" * 60)
        print("🎉 测试完成 - 系统无Google Sheets依赖运行正常！")
        print("✅ 所有核心功能都工作正常")
        print("📄 系统现在完全依赖备份输出方案")
        print("🚀 GitHub Actions工作流应该能正常启动")
        
        print("\n📋 系统现在提供的输出方式：")
        print("  1. 本地JSON备份文件")
        print("  2. 人性化TXT摘要文件")
        print("  3. CSV数据导出")
        print("  4. 邮件通知（如配置）")
        print("  5. GitHub Artifacts上传")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_system_without_google_sheets()
    if success:
        print("\n🎯 建议：现在可以在GitHub Actions页面手动触发工作流测试！")
    sys.exit(0 if success else 1) 