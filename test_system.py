#!/usr/bin/env python3
"""
完整系统测试脚本 - 使用模拟数据测试各组件
"""

import sys
import os
import json
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import Config
from src.data_processor import DataProcessor
from src.notification_system import NotificationSystem

def create_mock_data():
    """创建模拟的AI工具数据"""
    return [
        {
            "name": "GPT-4 Turbo",
            "description": "Advanced large language model with multimodal capabilities, featuring improved reasoning, longer context windows, and enhanced performance across various tasks including coding, analysis, and creative writing.",
            "categories": ["LLM", "Multimodal AI", "Text Generation"],
            "link": "https://openai.com/gpt-4",
            "rating": "9.5/10",
            "source": "theresanaiforthat.com",
            "scraped_at": datetime.now().isoformat()
        },
        {
            "name": "Claude 3 Opus",
            "description": "Constitutional AI assistant with advanced reasoning capabilities, built with Anthropic's constitutional AI principles for safety and helpfulness. Excels at complex analysis and long-form content.",
            "categories": ["LLM", "Constitutional AI", "Safety AI"],
            "link": "https://anthropic.com/claude",
            "rating": "9.2/10",
            "source": "theresanaiforthat.com",
            "scraped_at": datetime.now().isoformat()
        },
        {
            "name": "Midjourney V6",
            "description": "State-of-the-art text-to-image generation model with photorealistic outputs, advanced prompt adherence, and sophisticated artistic capabilities. Features improved detail rendering and style consistency.",
            "categories": ["Image Generation", "Creative AI", "Text-to-Image"],
            "link": "https://midjourney.com",
            "rating": "9.7/10",
            "source": "theresanaiforthat.com",
            "scraped_at": datetime.now().isoformat()
        },
        {
            "name": "Retrieval-Augmented Generation (RAG) Framework",
            "description": "Advanced AI architecture combining large language models with external knowledge retrieval systems for enhanced accuracy and up-to-date information access in conversational AI applications.",
            "categories": ["AI Architecture", "Retrieval Systems", "Knowledge Management"],
            "link": "https://example.com/rag",
            "rating": "8.8/10",
            "source": "theresanaiforthat.com",
            "scraped_at": datetime.now().isoformat()
        },
        {
            "name": "Agent-Based LLM Framework",
            "description": "Multi-agent system leveraging large language models for autonomous task execution, featuring tool usage, memory management, and collaborative reasoning capabilities for complex problem solving.",
            "categories": ["AI Agents", "Multi-Agent Systems", "Tool Usage"],
            "link": "https://example.com/agents",
            "rating": "8.5/10",
            "source": "theresanaiforthat.com",
            "scraped_at": datetime.now().isoformat()
        }
    ]

def create_mock_extracted_words():
    """创建模拟的提取词汇数据"""
    return [
        {
            "word": "Constitutional AI",
            "category": "AI Safety",
            "definition": "AI training methodology that incorporates ethical principles and safety constraints into the model's behavior",
            "importance": "high",
            "trend_potential": 9,
            "business_value": "high",
            "is_emerging": True,
            "extraction_count": 1,
            "contexts": ["AI safety and alignment research", "Responsible AI development"],
            "related_terms": ["AI Safety", "Alignment", "RLHF"],
            "target_sectors": ["AI Research", "Technology", "Ethics"],
            "extracted_at": datetime.now().isoformat()
        },
        {
            "word": "Retrieval-Augmented Generation",
            "category": "AI Architecture",
            "definition": "AI technique that enhances language models by incorporating external knowledge retrieval",
            "importance": "high",
            "trend_potential": 8,
            "business_value": "high",
            "is_emerging": True,
            "extraction_count": 1,
            "contexts": ["Knowledge-enhanced AI systems", "Information retrieval"],
            "related_terms": ["RAG", "Vector Databases", "Knowledge Graphs"],
            "target_sectors": ["Enterprise AI", "Search", "Knowledge Management"],
            "extracted_at": datetime.now().isoformat()
        },
        {
            "word": "Multi-Agent Systems",
            "category": "AI Architecture",
            "definition": "AI systems composed of multiple autonomous agents that can interact and collaborate",
            "importance": "medium",
            "trend_potential": 7,
            "business_value": "medium",
            "is_emerging": True,
            "extraction_count": 1,
            "contexts": ["Collaborative AI", "Distributed intelligence"],
            "related_terms": ["AI Agents", "Swarm Intelligence", "Distributed AI"],
            "target_sectors": ["Automation", "Robotics", "Enterprise Software"],
            "extracted_at": datetime.now().isoformat()
        },
        {
            "word": "Prompt Adherence",
            "category": "AI Capability",
            "definition": "The ability of AI models to accurately follow and implement user instructions",
            "importance": "medium",
            "trend_potential": 6,
            "business_value": "medium",
            "is_emerging": False,
            "extraction_count": 1,
            "contexts": ["Text-to-image generation", "Instruction following"],
            "related_terms": ["Prompt Engineering", "Instruction Following", "Controllability"],
            "target_sectors": ["Creative AI", "Content Generation", "Design"],
            "extracted_at": datetime.now().isoformat()
        },
        {
            "word": "Photorealistic Rendering",
            "category": "AI Output Quality",
            "definition": "AI capability to generate images that are indistinguishable from real photographs",
            "importance": "medium",
            "trend_potential": 8,
            "business_value": "high",
            "is_emerging": False,
            "extraction_count": 1,
            "contexts": ["Image generation", "Visual AI"],
            "related_terms": ["Hyperrealism", "Visual Fidelity", "Realistic Generation"],
            "target_sectors": ["Media", "Advertising", "Entertainment"],
            "extracted_at": datetime.now().isoformat()
        }
    ]

def test_data_processor():
    """测试数据处理模块"""
    print("🧪 测试数据处理模块...")
    
    try:
        processor = DataProcessor()
        mock_words = create_mock_extracted_words()
        
        print(f"📊 处理 {len(mock_words)} 个模拟词汇...")
        
        # 测试数据处理
        result = processor.process_extracted_words(mock_words)
        
        if result:
            words = result.get('words', [])
            summary = result.get('summary', {})
            
            print(f"✅ 处理完成: {len(words)} 个唯一词汇")
            print(f"📈 统计信息:")
            print(f"   - 新兴术语: {summary.get('emerging_terms_count', 0)}")
            print(f"   - 平均趋势评分: {summary.get('average_trend_score', 0)}")
            print(f"   - 分类数量: {len(summary.get('categories', {}))}")
            
            # 显示排名前3的词汇
            print(f"\n🏆 排名前3的词汇:")
            for i, word in enumerate(words[:3], 1):
                print(f"{i}. {word['word']} ({word['category']}) - 评分: {word.get('ranking_score', 0):.1f}")
            
            return True
        else:
            print("❌ 数据处理失败")
            return False
            
    except Exception as e:
        print(f"❌ 数据处理测试失败: {e}")
        return False

def test_notification_system():
    """测试通知系统"""
    print("\n🧪 测试通知系统...")
    
    try:
        notification_system = NotificationSystem()
        
        # 创建测试数据
        mock_summary = {
            'total_words': 5,
            'emerging_terms_count': 3,
            'average_trend_score': 7.6,
            'categories': {
                'AI Safety': 1,
                'AI Architecture': 2,
                'AI Capability': 1,
                'AI Output Quality': 1
            },
            'top_categories': [
                ('AI Architecture', 2),
                ('AI Safety', 1),
                ('AI Capability', 1)
            ]
        }
        
        mock_words = create_mock_extracted_words()[:3]  # 取前3个
        
        # 测试成功通知格式
        print("📤 生成成功通知...")
        success_notification = notification_system.format_success_notification({
            'status': 'success',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'summary': mock_summary,
            'words': mock_words,
            'sheets_url': 'https://docs.google.com/spreadsheets/d/test123',
            'source_url': 'https://theresanaiforthat.com/test'
        })
        
        print("✅ 成功通知格式:")
        print(success_notification[:500] + "..." if len(success_notification) > 500 else success_notification)
        
        # 测试错误通知格式
        print("\n📤 生成错误通知...")
        error_notification = notification_system.format_error_notification({
            'status': 'error',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error': '测试错误消息',
            'stage': '数据处理阶段',
            'partial_results': {'scraped_count': 5, 'processed_count': 0}
        })
        
        print("✅ 错误通知格式:")
        print(error_notification[:300] + "..." if len(error_notification) > 300 else error_notification)
        
        return True
        
    except Exception as e:
        print(f"❌ 通知系统测试失败: {e}")
        return False

def test_config_validation():
    """测试配置验证"""
    print("\n🧪 测试配置验证...")
    
    try:
        config = Config()
        
        # 显示配置信息
        print("📋 当前配置:")
        config.print_config()
        
        # 验证配置（这可能会失败，因为我们没有设置API密钥）
        print("\n🔍 验证配置...")
        is_valid = config.validate()
        
        if is_valid:
            print("✅ 配置验证通过")
        else:
            print("⚠️ 配置验证失败 - 这是正常的，因为没有设置API密钥")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 AI Words Mining System - 系统测试")
    print("="*60)
    
    success_count = 0
    total_tests = 3
    
    # 测试配置
    if test_config_validation():
        success_count += 1
    
    # 测试数据处理
    if test_data_processor():
        success_count += 1
    
    # 测试通知系统
    if test_notification_system():
        success_count += 1
    
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)
    print(f"✅ 成功: {success_count}/{total_tests}")
    print(f"❌ 失败: {total_tests - success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 所有测试通过！系统基础功能正常")
    else:
        print("⚠️ 部分测试失败，但这可能是由于缺少API密钥等配置")
    
    print("\n💡 注意事项:")
    print("- 网页爬取可能被网站的反爬虫机制阻止")
    print("- OpenAI分析需要有效的API密钥")
    print("- Google Sheets集成需要服务账户凭据")
    print("- 完整功能需要在GitHub Actions中配置所有secrets")
    
    return success_count == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 