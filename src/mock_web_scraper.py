#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from datetime import datetime, timedelta
import config

class MockWebScraper:
    """
    模拟Web爬虫 - 生成测试数据
    """
    
    def __init__(self):
        self.config = config.Config()
        
    def scrape_ai_tools(self, url=None):
        """
        模拟爬取AI工具数据
        """
        print(f"🎭 模拟爬取AI工具数据...")
        
        # 模拟AI工具数据
        mock_tools = [
            {
                'name': 'ChatGPT',
                'description': 'Advanced AI chatbot for natural language conversations and task assistance',
                'link': 'https://chat.openai.com',
                'category': 'AI Assistant',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 1
            },
            {
                'name': 'Midjourney',
                'description': 'AI-powered image generation tool for creating artistic visuals',
                'link': 'https://midjourney.com',
                'category': 'Image Generation',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 2
            },
            {
                'name': 'Notion AI',
                'description': 'AI-enhanced productivity platform for note-taking and collaboration',
                'link': 'https://notion.so',
                'category': 'Productivity',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 3
            },
            {
                'name': 'GitHub Copilot',
                'description': 'AI pair programmer that helps you write code faster and with fewer errors',
                'link': 'https://github.com/features/copilot',
                'category': 'Development',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 4
            },
            {
                'name': 'Claude',
                'description': 'AI assistant for analysis, writing, math, coding, and creative tasks',
                'link': 'https://claude.ai',
                'category': 'AI Assistant',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 5
            },
            {
                'name': 'Stable Diffusion',
                'description': 'Open-source deep learning text-to-image model for generating images',
                'link': 'https://stability.ai',
                'category': 'Image Generation',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 6
            },
            {
                'name': 'Jasper AI',
                'description': 'AI content generation platform for marketing and business writing',
                'link': 'https://jasper.ai',
                'category': 'Content Creation',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 7
            },
            {
                'name': 'Grammarly',
                'description': 'AI-powered writing assistant for grammar, spelling, and style improvements',
                'link': 'https://grammarly.com',
                'category': 'Writing',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 8
            },
            {
                'name': 'Canva AI',
                'description': 'AI-enhanced design platform for creating graphics, presentations, and more',
                'link': 'https://canva.com',
                'category': 'Design',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 9
            },
            {
                'name': 'Runway ML',
                'description': 'Creative AI platform for video editing, image generation, and machine learning',
                'link': 'https://runwayml.com',
                'category': 'Creative AI',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 10
            },
            {
                'name': 'Luma AI',
                'description': 'AI-powered 3D capture and neural rendering technology',
                'link': 'https://lumalabs.ai',
                'category': '3D & AR',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 11
            },
            {
                'name': 'Perplexity AI',
                'description': 'AI search engine that provides accurate answers with citations',
                'link': 'https://perplexity.ai',
                'category': 'Search',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 12
            },
            {
                'name': 'Anthropic Claude',
                'description': 'Constitutional AI system designed to be helpful, harmless, and honest',
                'link': 'https://anthropic.com',
                'category': 'AI Assistant',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 13
            },
            {
                'name': 'Synthesia',
                'description': 'AI video generation platform for creating videos with AI avatars',
                'link': 'https://synthesia.io',
                'category': 'Video Generation',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 14
            },
            {
                'name': 'ElevenLabs',
                'description': 'AI voice generation platform for creating realistic speech synthesis',
                'link': 'https://elevenlabs.io',
                'category': 'Voice AI',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 15
            },
            {
                'name': 'Replicate',
                'description': 'Platform for running and deploying machine learning models in the cloud',
                'link': 'https://replicate.com',
                'category': 'ML Platform',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 16
            },
            {
                'name': 'Hugging Face',
                'description': 'Open-source platform for machine learning models and datasets',
                'link': 'https://huggingface.co',
                'category': 'ML Platform',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 17
            },
            {
                'name': 'Gamma',
                'description': 'AI-powered presentation generator for creating slides and documents',
                'link': 'https://gamma.app',
                'category': 'Presentation',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 18
            },
            {
                'name': 'Pika Labs',
                'description': 'AI video generation platform for creating short video clips',
                'link': 'https://pika.art',
                'category': 'Video Generation',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 19
            },
            {
                'name': 'Replit AI',
                'description': 'AI-powered coding assistant integrated into online development environment',
                'link': 'https://replit.com',
                'category': 'Development',
                'source': 'theresanaiforthat.com',
                'scraped_at': datetime.now().isoformat(),
                'index': 20
            }
        ]
        
        # 随机选择工具数量
        num_tools = random.randint(15, 20)
        selected_tools = random.sample(mock_tools, num_tools)
        
        # 添加一些随机变化
        for tool in selected_tools:
            # 随机调整时间戳
            random_time = datetime.now() - timedelta(hours=random.randint(0, 24))
            tool['scraped_at'] = random_time.isoformat()
            
            # 随机调整一些描述
            if random.random() < 0.3:  # 30%的概率
                tool['description'] = tool['description'] + f" (Updated: {random_time.strftime('%Y-%m-%d')})"
        
        print(f"✅ 模拟生成了 {len(selected_tools)} 个AI工具")
        return selected_tools 