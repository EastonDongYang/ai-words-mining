#!/usr/bin/env python3
"""
测试优化后的OpenAI prompt效果
"""

import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import Config
from src.openai_analyzer import OpenAIAnalyzer

def create_test_data():
    """创建测试数据"""
    return [
        {
            'name': 'AI Code Assistant',
            'description': 'An AI-powered coding assistant that uses retrieval-augmented generation (RAG) to help developers write better code. Features include multimodal code analysis, prompt engineering assistance, and automated documentation generation.',
            'categories': ['Developer Tools', 'AI Assistant']
        },
        {
            'name': 'Smart Content Creator',
            'description': 'AI tool for content creators that enables zero-shot learning for video editing, supports synthetic media generation, and offers real-time collaboration features for distributed teams.',
            'categories': ['Content Creation', 'AI Tools']
        },
        {
            'name': 'Voice Clone Studio',
            'description': 'Advanced voice cloning technology using few-shot learning techniques. Supports emotional voice synthesis, cross-lingual voice conversion, and offers edge computing deployment for privacy-focused applications.',
            'categories': ['Audio AI', 'Voice Technology']
        },
        {
            'name': 'Vision AI Platform',
            'description': 'Computer vision platform featuring foundation models for object detection, supports federated learning for privacy-preserving training, and includes explainable AI features for model interpretability.',
            'categories': ['Computer Vision', 'AI Platform']
        },
        {
            'name': 'Text Analytics Pro',
            'description': 'Natural language processing tool with advanced semantic search capabilities, supports agentic AI workflows, and features automated reasoning for complex text analysis tasks.',
            'categories': ['NLP', 'Text Analysis']
        }
    ]

def test_new_prompt():
    """测试新的prompt效果"""
    print("🧪 测试优化后的OpenAI prompt...")
    
    # 检查配置
    config = Config()
    if not config.OPENAI_API_KEY:
        print("❌ 请设置OpenAI API Key")
        return False
    
    # 创建分析器
    analyzer = OpenAIAnalyzer()
    
    # 创建测试数据
    test_data = create_test_data()
    
    print(f"📊 使用 {len(test_data)} 个测试工具进行分析...")
    
    try:
        # 分析测试数据
        results = analyzer.analyze_and_extract(test_data)
        
        if results:
            print(f"\n✅ 成功提取 {len(results)} 个概念性词汇:")
            print("="*80)
            
            for i, word_data in enumerate(results, 1):
                print(f"\n🔍 #{i}. {word_data['word']}")
                print(f"   分类: {word_data['category']}")
                print(f"   定义: {word_data['definition']}")
                print(f"   重要性: {word_data['importance']}")
                print(f"   趋势潜力: {word_data['trend_potential']}/10")
                print(f"   商业价值: {word_data['business_value']}")
                print(f"   新兴概念: {'✅' if word_data.get('is_emerging', False) else '❌'}")
                print(f"   排名分数: {word_data.get('ranking_score', 0):.1f}")
                print(f"   上下文: {word_data['context']}")
            
            # 分析结果质量
            print("\n📈 结果质量分析:")
            emerging_count = sum(1 for w in results if w.get('is_emerging', False))
            high_trend_count = sum(1 for w in results if w.get('trend_potential', 5) >= 7)
            high_business_count = sum(1 for w in results if w.get('business_value', 'medium') == 'high')
            
            print(f"   - 新兴概念: {emerging_count}/{len(results)} ({emerging_count/len(results)*100:.1f}%)")
            print(f"   - 高趋势潜力 (≥7): {high_trend_count}/{len(results)} ({high_trend_count/len(results)*100:.1f}%)")
            print(f"   - 高商业价值: {high_business_count}/{len(results)} ({high_business_count/len(results)*100:.1f}%)")
            
            # 检查是否包含产品名称
            product_names = ['chatgpt', 'claude', 'midjourney', 'gpt-4', 'dall-e', 'stable diffusion']
            found_products = [w['word'] for w in results if any(p in w['word'].lower() for p in product_names)]
            
            if found_products:
                print(f"\n⚠️ 发现产品名称: {found_products}")
            else:
                print(f"\n✅ 没有发现产品名称，过滤效果良好")
            
            # 按类别统计
            categories = {}
            for word_data in results:
                category = word_data['category']
                categories[category] = categories.get(category, 0) + 1
            
            print(f"\n📊 按类别统计:")
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                print(f"   - {category}: {count} 个")
            
            return True
            
        else:
            print("❌ 没有提取到任何词汇")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def compare_with_old_results():
    """与旧版本结果对比"""
    print("\n💡 优化效果对比:")
    print("🔴 旧版本问题:")
    print("   - 提取产品名称 (ChatGPT、Claude、Midjourney等)")
    print("   - 包含版本号 (V6、XL、Pro等)")
    print("   - 缺乏趋势价值评估")
    print("   - 不适合Google Trends分析")
    
    print("\n🟢 新版本改进:")
    print("   - 专注概念性词汇，过滤产品名称")
    print("   - 添加趋势潜力评估 (1-10分)")
    print("   - 添加商业价值评估")
    print("   - 识别新兴概念标志")
    print("   - 适合Google Trends分析和建站")

def main():
    """主函数"""
    print("🚀 测试优化后的OpenAI prompt效果...")
    print("="*60)
    
    try:
        success = test_new_prompt()
        
        if success:
            compare_with_old_results()
            
            print("\n✅ 测试完成!")
            print("\n🎯 现在系统会提取:")
            print("   - 真正的新兴概念 (如：检索增强生成、多模态分析)")
            print("   - 技术方法论 (如：零样本学习、联邦学习)")
            print("   - 应用场景新词 (如：边缘计算部署、隐私保护训练)")
            print("   - 行业发展趋势 (如：代理AI工作流、可解释AI)")
            
            print("\n💡 建议:")
            print("   1. 定期更新产品名称过滤列表")
            print("   2. 根据实际效果调整趋势潜力阈值")
            print("   3. 考虑添加更多评估维度")
            print("   4. 定期验证Google Trends搜索效果")
            
        else:
            print("\n❌ 测试失败，请检查配置")
            
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 