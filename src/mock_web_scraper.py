"""
Mock Web Scraper for AI Words Mining System
用于在真实爬虫失败时提供模拟数据的模块
"""

import random
from typing import List, Dict
from datetime import datetime

class MockWebScraper:
    """模拟网络爬虫，提供测试数据"""
    
    def __init__(self):
        self.mock_tools = [
            {
                "name": "ChatGPT-4",
                "description": "Advanced conversational AI model with enhanced reasoning capabilities and multimodal support",
                "categories": ["AI Chat", "Language Model", "Conversational AI"],
                "url": "https://openai.com/chatgpt",
                "features": ["Natural language processing", "Code generation", "Creative writing"]
            },
            {
                "name": "Claude-3",
                "description": "Next-generation AI assistant with advanced reasoning and safety features",
                "categories": ["AI Assistant", "Language Model", "Safety AI"],
                "url": "https://anthropic.com/claude",
                "features": ["Constitutional AI", "Long context", "Harmlessness"]
            },
            {
                "name": "Midjourney V6",
                "description": "Advanced AI image generation tool with photorealistic capabilities",
                "categories": ["Image Generation", "Creative AI", "Art Generation"],
                "url": "https://midjourney.com",
                "features": ["Photorealistic images", "Style transfer", "Artistic rendering"]
            },
            {
                "name": "Runway ML",
                "description": "AI video generation and editing platform with real-time capabilities",
                "categories": ["Video AI", "Content Creation", "Media Generation"],
                "url": "https://runwayml.com",
                "features": ["Video generation", "Real-time editing", "Style transfer"]
            },
            {
                "name": "Perplexity AI",
                "description": "AI-powered search engine that provides conversational answers with citations",
                "categories": ["Search AI", "Research Tool", "Information Retrieval"],
                "url": "https://perplexity.ai",
                "features": ["Conversational search", "Source citations", "Real-time information"]
            },
            {
                "name": "Sora",
                "description": "OpenAI's text-to-video generation model with realistic motion and physics",
                "categories": ["Video Generation", "Generative AI", "Media Creation"],
                "url": "https://openai.com/sora",
                "features": ["Text-to-video", "Realistic physics", "Long-form content"]
            },
            {
                "name": "Gemini Ultra",
                "description": "Google's most capable multimodal AI model with advanced reasoning",
                "categories": ["Multimodal AI", "Language Model", "Google AI"],
                "url": "https://deepmind.google/gemini",
                "features": ["Multimodal understanding", "Code generation", "Mathematical reasoning"]
            },
            {
                "name": "Stable Diffusion XL",
                "description": "Open-source image generation model with improved quality and control",
                "categories": ["Image Generation", "Open Source", "Diffusion Models"],
                "url": "https://stability.ai",
                "features": ["High resolution", "Fine-tuning", "Community models"]
            },
            {
                "name": "LangChain",
                "description": "Framework for developing applications powered by language models",
                "categories": ["AI Framework", "Development Tool", "LLM Integration"],
                "url": "https://langchain.com",
                "features": ["Chain operations", "Memory management", "Tool integration"]
            },
            {
                "name": "AutoGPT",
                "description": "Autonomous AI agent that can perform tasks with minimal human intervention",
                "categories": ["AI Agent", "Automation", "Autonomous Systems"],
                "url": "https://github.com/Significant-Gravitas/AutoGPT",
                "features": ["Task automation", "Goal-oriented", "Self-directed"]
            },
            {
                "name": "Copilot X",
                "description": "Next-generation AI pair programmer with enhanced code understanding",
                "categories": ["Code Assistant", "Programming AI", "Developer Tools"],
                "url": "https://github.com/features/copilot",
                "features": ["Code completion", "Bug detection", "Code explanation"]
            },
            {
                "name": "Whisper Large",
                "description": "Advanced speech recognition model with multilingual support",
                "categories": ["Speech AI", "Audio Processing", "Transcription"],
                "url": "https://openai.com/whisper",
                "features": ["Multilingual", "Real-time transcription", "High accuracy"]
            }
        ]
    
    def scrape_ai_tools(self, max_tools: int = 8) -> List[Dict]:
        """
        返回模拟的AI工具数据
        
        Args:
            max_tools: 最大返回工具数量
            
        Returns:
            List[Dict]: 模拟的AI工具数据列表
        """
        print("🔧 使用模拟数据模式...")
        
        # 随机选择工具
        selected_tools = random.sample(self.mock_tools, min(max_tools, len(self.mock_tools)))
        
        # 添加时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for tool in selected_tools:
            tool['scraped_at'] = timestamp
            tool['source'] = 'mock_data'
        
        print(f"✅ 模拟数据已生成：{len(selected_tools)} 个AI工具")
        return selected_tools
    
    def get_trending_categories(self) -> List[str]:
        """获取热门类别"""
        return [
            "Generative AI",
            "Large Language Models",
            "Multimodal AI",
            "AI Agents",
            "Computer Vision",
            "Natural Language Processing",
            "Audio AI",
            "Video Generation",
            "Code Generation",
            "AI Safety"
        ]
    
    def get_emerging_terms(self) -> List[Dict]:
        """获取新兴术语"""
        return [
            {
                "term": "Retrieval-Augmented Generation",
                "category": "AI Technique",
                "description": "RAG系统结合检索和生成来提供更准确的回答"
            },
            {
                "term": "Constitutional AI",
                "category": "AI Safety",
                "description": "通过宪法原则训练的AI系统，提高安全性和可靠性"
            },
            {
                "term": "Mixture of Experts",
                "category": "Model Architecture",
                "description": "MoE架构通过专家网络提高模型效率"
            },
            {
                "term": "Chain-of-Thought",
                "category": "Reasoning Technique",
                "description": "CoT提示技术帮助AI进行逐步推理"
            },
            {
                "term": "Multimodal Fusion",
                "category": "AI Technique",
                "description": "多模态融合技术整合不同类型的数据输入"
            }
        ] 