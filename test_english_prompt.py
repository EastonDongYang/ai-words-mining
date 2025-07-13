#!/usr/bin/env python3
"""
Test English Prompt for Extracting English Emerging Terms
"""

import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import Config
from src.openai_analyzer import OpenAIAnalyzer

def create_test_data():
    """Create test data with rich technical descriptions"""
    return [
        {
            'name': 'AI Code Assistant',
            'description': 'An AI-powered coding assistant that uses retrieval-augmented generation (RAG) to help developers write better code. Features include multimodal code analysis, prompt engineering assistance, and automated documentation generation using foundation models.',
            'categories': ['Developer Tools', 'AI Assistant']
        },
        {
            'name': 'Smart Content Creator',
            'description': 'AI tool for content creators that enables zero-shot learning for video editing, supports synthetic media generation, and offers real-time collaboration features for distributed teams using edge computing.',
            'categories': ['Content Creation', 'AI Tools']
        },
        {
            'name': 'Voice Clone Studio',
            'description': 'Advanced voice cloning technology using few-shot learning techniques. Supports emotional voice synthesis, cross-lingual voice conversion, and offers edge deployment for privacy-preserving applications.',
            'categories': ['Audio AI', 'Voice Technology']
        },
        {
            'name': 'Vision AI Platform',
            'description': 'Computer vision platform featuring foundation models for object detection, supports federated learning for privacy-preserving training, and includes explainable AI features for model interpretability and human-in-the-loop workflows.',
            'categories': ['Computer Vision', 'AI Platform']
        },
        {
            'name': 'Text Analytics Pro',
            'description': 'Natural language processing tool with advanced semantic search capabilities, supports agentic AI workflows, automated reasoning for complex text analysis, and features prompt chaining for multi-step analysis.',
            'categories': ['NLP', 'Text Analysis']
        },
        {
            'name': 'AutoML Designer',
            'description': 'No-code machine learning platform that enables citizen data scientists to build models using neural architecture search, automated feature engineering, and supports democratized AI development.',
            'categories': ['Machine Learning', 'No-Code']
        }
    ]

def test_english_extraction():
    """Test English term extraction"""
    print("🧪 Testing English Prompt for Emerging Term Extraction...")
    
    # Check configuration
    config = Config()
    if not config.OPENAI_API_KEY:
        print("❌ Please set OpenAI API Key")
        return False
    
    # Create analyzer
    analyzer = OpenAIAnalyzer()
    
    # Create test data
    test_data = create_test_data()
    
    print(f"📊 Analyzing {len(test_data)} test tools...")
    
    try:
        # Analyze test data
        results = analyzer.analyze_and_extract(test_data)
        
        if results:
            print(f"\n✅ Successfully extracted {len(results)} English concepts:")
            print("="*80)
            
            for i, word_data in enumerate(results, 1):
                print(f"\n🔍 #{i}. {word_data['word']}")
                print(f"   Category: {word_data['category']}")
                print(f"   Definition: {word_data['definition']}")
                print(f"   Importance: {word_data['importance']}")
                print(f"   Trend Potential: {word_data['trend_potential']}/10")
                print(f"   Business Value: {word_data['business_value']}")
                print(f"   Emerging: {'✅' if word_data.get('is_emerging', False) else '❌'}")
                print(f"   Ranking Score: {word_data.get('ranking_score', 0):.1f}")
                print(f"   Context: {word_data['context']}")
            
            # Quality analysis
            print("\n📈 Quality Analysis:")
            emerging_count = sum(1 for w in results if w.get('is_emerging', False))
            high_trend_count = sum(1 for w in results if w.get('trend_potential', 5) >= 7)
            high_business_count = sum(1 for w in results if w.get('business_value', 'medium') == 'high')
            
            print(f"   - Emerging Concepts: {emerging_count}/{len(results)} ({emerging_count/len(results)*100:.1f}%)")
            print(f"   - High Trend Potential (≥7): {high_trend_count}/{len(results)} ({high_trend_count/len(results)*100:.1f}%)")
            print(f"   - High Business Value: {high_business_count}/{len(results)} ({high_business_count/len(results)*100:.1f}%)")
            
            # Check for product names
            product_names = ['chatgpt', 'claude', 'midjourney', 'gpt-4', 'dall-e', 'stable diffusion', 'openai']
            found_products = [w['word'] for w in results if any(p in w['word'].lower() for p in product_names)]
            
            if found_products:
                print(f"\n⚠️ Found Product Names: {found_products}")
            else:
                print(f"\n✅ No product names found - filtering working well")
            
            # Check language (English validation)
            non_english_words = []
            for word_data in results:
                word = word_data['word']
                # Simple check for non-English characters
                if any(ord(char) > 127 for char in word):
                    non_english_words.append(word)
            
            if non_english_words:
                print(f"\n⚠️ Non-English terms found: {non_english_words}")
            else:
                print(f"\n✅ All terms are in English")
            
            # Category statistics
            categories = {}
            for word_data in results:
                category = word_data['category']
                categories[category] = categories.get(category, 0) + 1
            
            print(f"\n📊 Category Statistics:")
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                print(f"   - {category}: {count} terms")
            
            # Expected emerging terms validation
            expected_terms = [
                'retrieval-augmented generation', 'rag', 'multimodal',
                'zero-shot learning', 'few-shot learning', 'synthetic media',
                'edge computing', 'edge deployment', 'federated learning',
                'explainable ai', 'human-in-the-loop', 'agentic ai',
                'prompt engineering', 'prompt chaining', 'foundation models',
                'neural architecture search', 'democratized ai', 'citizen data scientists'
            ]
            
            found_expected = []
            for word_data in results:
                word_lower = word_data['word'].lower()
                for expected in expected_terms:
                    if expected in word_lower or word_lower in expected:
                        found_expected.append(word_data['word'])
                        break
            
            print(f"\n🎯 Expected Emerging Terms Found: {len(found_expected)}")
            for term in found_expected:
                print(f"   ✅ {term}")
            
            return True
            
        else:
            print("❌ No terms extracted")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def compare_language_effectiveness():
    """Compare English vs Chinese prompt effectiveness"""
    print("\n💡 Language Optimization Benefits:")
    print("🔴 Previous Chinese Issues:")
    print("   - Mixed language results")
    print("   - Poor Google Trends compatibility")
    print("   - Limited international SEO value")
    print("   - Inconsistent terminology")
    
    print("\n🟢 New English Advantages:")
    print("   - Pure English conceptual terms")
    print("   - Optimized for Google Trends analysis")
    print("   - International market compatibility")
    print("   - Better for global keyword research")
    print("   - Consistent technical terminology")

def main():
    """Main function"""
    print("🚀 Testing English Prompt for Emerging Terms...")
    print("="*60)
    
    try:
        success = test_english_extraction()
        
        if success:
            compare_language_effectiveness()
            
            print("\n✅ English Prompt Test Completed!")
            print("\n🎯 Expected English Terms:")
            print("   - Retrieval-Augmented Generation (RAG)")
            print("   - Zero-Shot Learning")
            print("   - Federated Learning")
            print("   - Edge Computing")
            print("   - Explainable AI")
            print("   - Human-in-the-Loop")
            print("   - Agentic AI Workflows")
            print("   - Prompt Engineering")
            print("   - Foundation Models")
            print("   - Neural Architecture Search")
            
            print("\n💡 Google Trends Ready:")
            print("   1. All terms are in English")
            print("   2. Conceptual rather than product-specific")
            print("   3. Emerging trends with search potential")
            print("   4. Business value for website development")
            
        else:
            print("\n❌ Test failed, please check configuration")
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 