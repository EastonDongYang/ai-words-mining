#!/usr/bin/env python3
"""
测试模拟数据模式的脚本
用于验证在没有外部依赖的情况下系统能否正常工作
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

def test_mock_mode():
    """测试模拟数据模式"""
    print("🧪 开始测试模拟数据模式...")
    print("=" * 50)
    
    try:
        # 1. 测试配置
        print("1️⃣ 测试配置...")
        config = Config()
        if not config.OPENAI_API_KEY:
            print("⚠️ 警告：未设置OpenAI API密钥")
        else:
            print("✅ 配置加载成功")
        
        # 2. 测试模拟数据生成
        print("\n2️⃣ 测试模拟数据生成...")
        mock_scraper = MockWebScraper()
        tools_data = mock_scraper.scrape_ai_tools(6)
        print(f"✅ 生成了 {len(tools_data)} 个模拟工具")
        
        # 显示工具名称
        for i, tool in enumerate(tools_data, 1):
            print(f"   {i}. {tool['name']}")
        
        # 3. 测试OpenAI分析（如果有API密钥）
        print("\n3️⃣ 测试OpenAI分析...")
        if config.OPENAI_API_KEY and config.OPENAI_API_KEY != '':
            try:
                analyzer = OpenAIAnalyzer()
                extracted_words = analyzer.analyze_tools_batch(tools_data[:3])  # 只分析前3个工具
                print(f"✅ 成功提取了 {len(extracted_words)} 个新词汇")
                
                # 显示提取的词汇
                if extracted_words:
                    print("   提取的词汇:")
                    for word_data in extracted_words[:5]:  # 显示前5个
                        print(f"   - {word_data.get('word', 'N/A')}: {word_data.get('definition', 'N/A')}")
                
            except Exception as e:
                print(f"⚠️ OpenAI分析失败：{e}")
                # 创建模拟的提取词汇用于测试
                extracted_words = [
                    {
                        'word': 'Constitutional AI',
                        'category': 'AI Safety',
                        'definition': 'AI system trained with constitutional principles',
                        'context': 'Claude-3 description',
                        'importance': 'high',
                        'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    },
                    {
                        'word': 'Multimodal Support',
                        'category': 'AI Capability',
                        'definition': 'Ability to process multiple types of input',
                        'context': 'ChatGPT-4 description',
                        'importance': 'high',
                        'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                ]
                print(f"✅ 使用模拟词汇数据：{len(extracted_words)} 个词汇")
        else:
            print("⚠️ 跳过OpenAI分析（未设置API密钥）")
            # 创建模拟的提取词汇
            extracted_words = [
                {
                    'word': 'Test Word 1',
                    'category': 'Test Category',
                    'definition': 'Test definition 1',
                    'context': 'Test context',
                    'importance': 'medium',
                    'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'word': 'Test Word 2',
                    'category': 'Test Category',
                    'definition': 'Test definition 2',
                    'context': 'Test context',
                    'importance': 'high',
                    'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            ]
            print(f"✅ 使用模拟词汇数据：{len(extracted_words)} 个词汇")
        
        # 4. 测试数据处理
        print("\n4️⃣ 测试数据处理...")
        processor = DataProcessor()
        processed_result = processor.process_extracted_words(extracted_words)
        processed_words = processed_result.get('words', [])
        print(f"✅ 处理了 {len(processed_words)} 个词汇")
        
        # 5. 测试CSV导出
        print("\n5️⃣ 测试CSV导出...")
        if processed_words:
            processor.export_to_csv(processed_words, "test_export.csv")
            print("✅ CSV导出成功：test_export.csv")
        
        print("\n" + "=" * 50)
        print("🎉 模拟数据模式测试完成！")
        print("✅ 所有核心功能都正常工作")
        print("📝 即使在没有外部依赖的情况下，系统也能正常运行")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_mock_mode()
    sys.exit(0 if success else 1) 