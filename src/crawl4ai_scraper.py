#!/usr/bin/env python3
"""
Crawl4AI Enhanced Scraper for AI Words Mining System
基于crawl4ai的高性能AI工具爬虫
"""

import asyncio
import json
import time
from typing import List, Dict, Optional, Any
from datetime import datetime
from urllib.parse import urljoin, urlparse
from pydantic import BaseModel, Field

# Crawl4AI imports - 修正导入语句
try:
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
    from crawl4ai.extraction_strategy import JsonCssExtractionStrategy, LLMExtractionStrategy
    from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter
    from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
except ImportError as e:
    print(f"❌ Crawl4AI导入错误: {e}")
    print("请确保已安装crawl4ai: pip install crawl4ai")
    raise

from config import Config


class AIToolExtractor:
    """AI工具信息提取器"""
    
    def __init__(self):
        self.config = Config()
        
    def get_toolify_schema(self) -> dict:
        """Toolify.ai的提取schema"""
        return {
            "name": "Toolify AI Tools",
            "baseSelector": ".tool-card, .tool-item, .grid-item",
            "fields": [
                {
                    "name": "tool_name",
                    "selector": "h3, h4, .tool-name, .title, a[href*='/tool/']",
                    "type": "text",
                },
                {
                    "name": "description",
                    "selector": ".description, .tool-description, p",
                    "type": "text",
                },
                {
                    "name": "link",
                    "selector": "a[href*='/tool/'], a[href*='/ai/']",
                    "type": "attribute",
                    "attribute": "href"
                },
                {
                    "name": "categories",
                    "selector": ".tag, .category, .badge, .label",
                    "type": "list",
                    "fields": [
                        {"name": "category", "selector": "", "type": "text"}
                    ]
                }
            ]
        }
    
    def get_producthunt_schema(self) -> dict:
        """Product Hunt的提取schema"""
        return {
            "name": "Product Hunt Tools",
            "baseSelector": "[data-test*='post'], .item, .product-item",
            "fields": [
                {
                    "name": "tool_name",
                    "selector": "h3, h4, .name, .title, a[data-test*='post-name']",
                    "type": "text",
                },
                {
                    "name": "description",
                    "selector": ".description, .tagline, p",
                    "type": "text",
                },
                {
                    "name": "link",
                    "selector": "a[href*='/posts/']",
                    "type": "attribute",
                    "attribute": "href"
                },
                {
                    "name": "upvotes",
                    "selector": ".vote-count, .upvote",
                    "type": "text",
                }
            ]
        }
    
    def get_futuretools_schema(self) -> dict:
        """Future Tools的提取schema"""
        return {
            "name": "Future Tools",
            "baseSelector": ".tool-card, .tool-item, .grid-item",
            "fields": [
                {
                    "name": "tool_name",
                    "selector": "h3, h4, .tool-name, .title",
                    "type": "text",
                },
                {
                    "name": "description",
                    "selector": ".description, .tool-description, p",
                    "type": "text",
                },
                {
                    "name": "link",
                    "selector": "a",
                    "type": "attribute",
                    "attribute": "href"
                },
                {
                    "name": "pricing",
                    "selector": ".price, .pricing, .cost",
                    "type": "text",
                }
            ]
        }


class AIToolModel(BaseModel):
    """AI工具数据模型（用于LLM提取）"""
    tool_name: str = Field(..., description="AI工具的名称")
    description: str = Field(..., description="工具的详细描述")
    categories: List[str] = Field(default_factory=list, description="工具的分类标签")
    pricing: Optional[str] = Field(None, description="定价信息")
    features: List[str] = Field(default_factory=list, description="主要功能特点")
    link: Optional[str] = Field(None, description="工具链接")


class Crawl4AIScraper:
    """基于Crawl4AI的高性能爬虫"""
    
    def __init__(self, debug_mode: bool = False):
        self.config = Config()
        self.debug_mode = debug_mode
        self.extractor = AIToolExtractor()
        
        # 浏览器配置
        self.browser_config = BrowserConfig(
            headless=True,
            verbose=debug_mode,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            java_script_enabled=True,
            # 反爬配置
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            # 使用持久化上下文避免重复初始化
            user_data_dir="./browser_profile",
            use_persistent_context=True,
        )
    
    async def scrape_site_with_css(self, url: str, site_name: str, max_items: int = 50) -> List[Dict]:
        """使用CSS选择器策略爬取网站"""
        
        # 根据网站选择schema
        schema_map = {
            "toolify": self.extractor.get_toolify_schema(),
            "producthunt": self.extractor.get_producthunt_schema(),
            "futuretools": self.extractor.get_futuretools_schema(),
        }
        
        schema = schema_map.get(site_name, self.extractor.get_toolify_schema())
        
        # 创建提取策略
        extraction_strategy = JsonCssExtractionStrategy(
            schema=schema,
            verbose=self.debug_mode
        )
        
        # 创建Markdown生成器（带内容过滤）
        markdown_generator = DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(
                threshold=0.48,
                threshold_type="fixed",
                min_word_threshold=10
            )
        )
        
        # 爬取配置
        crawl_config = CrawlerRunConfig(
            cache_mode=CacheMode.ENABLED,
            extraction_strategy=extraction_strategy,
            markdown_generator=markdown_generator,
            output_formats=['extracted_content', 'markdown'],
            # 等待动态内容加载
            wait_for_timeout=3000,
            # 执行滚动以加载更多内容
            js_code=[
                "window.scrollTo(0, document.body.scrollHeight);",
                "await new Promise(resolve => setTimeout(resolve, 2000));",
                "window.scrollTo(0, document.body.scrollHeight);"
            ],
            # 截图用于调试
            screenshot=self.debug_mode,
        )
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            if self.debug_mode:
                print(f"🕷️ 开始爬取: {site_name} - {url}")
            
            result = await crawler.arun(url=url, config=crawl_config)
            
            if result.success and result.extracted_content:
                try:
                    extracted_data = json.loads(result.extracted_content)
                    
                    # 数据清洗和标准化
                    cleaned_data = self.clean_and_standardize_data(
                        extracted_data, site_name, max_items
                    )
                    
                    if self.debug_mode:
                        print(f"✅ 成功从 {site_name} 提取 {len(cleaned_data)} 个工具")
                    
                    return cleaned_data
                
                except json.JSONDecodeError as e:
                    print(f"❌ JSON解析错误 ({site_name}): {e}")
                    return []
            else:
                print(f"❌ 爬取失败 ({site_name}): {result.error_message}")
                return []
    
    async def scrape_site_with_llm(self, url: str, site_name: str, max_items: int = 50) -> List[Dict]:
        """使用LLM策略爬取网站（需要API key）"""
        
        if not self.config.OPENAI_API_KEY:
            print("⚠️ 未配置OpenAI API Key，跳过LLM提取")
            return []
        
        # 创建LLM提取策略
        llm_strategy = LLMExtractionStrategy(
            provider="openai/gpt-4o-mini",  # 使用更便宜的模型
            api_token=self.config.OPENAI_API_KEY,
            schema=AIToolModel.schema(),
            extraction_type="schema",
            instruction=f"""
            从网页内容中提取AI工具信息。每个工具应包含：
            1. 工具名称（tool_name）
            2. 详细描述（description）
            3. 分类标签（categories）
            4. 定价信息（pricing，如果有）
            5. 主要功能特点（features）
            6. 工具链接（link）
            
            请确保提取的工具名称清晰、描述准确。忽略导航链接、广告等无关内容。
            最多提取 {max_items} 个工具。
            """,
            # 使用BM25过滤相关内容
            content_filter=BM25ContentFilter(
                user_query="AI tools artificial intelligence machine learning",
                bm25_threshold=1.0
            )
        )
        
        # 爬取配置
        crawl_config = CrawlerRunConfig(
            cache_mode=CacheMode.ENABLED,
            extraction_strategy=llm_strategy,
            output_formats=['extracted_content', 'markdown'],
            wait_for_timeout=3000,
            js_code=[
                "window.scrollTo(0, document.body.scrollHeight);",
                "await new Promise(resolve => setTimeout(resolve, 2000));"
            ],
        )
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            if self.debug_mode:
                print(f"🤖 使用LLM爬取: {site_name} - {url}")
            
            result = await crawler.arun(url=url, config=crawl_config)
            
            if result.success and result.extracted_content:
                try:
                    extracted_data = json.loads(result.extracted_content)
                    
                    # 如果是单个对象，转换为列表
                    if isinstance(extracted_data, dict):
                        extracted_data = [extracted_data]
                    
                    # 数据清洗和标准化
                    cleaned_data = self.clean_and_standardize_data(
                        extracted_data, site_name, max_items
                    )
                    
                    if self.debug_mode:
                        print(f"✅ LLM成功从 {site_name} 提取 {len(cleaned_data)} 个工具")
                    
                    return cleaned_data
                
                except json.JSONDecodeError as e:
                    print(f"❌ LLM JSON解析错误 ({site_name}): {e}")
                    return []
            else:
                print(f"❌ LLM爬取失败 ({site_name}): {result.error_message}")
                return []
    
    def clean_and_standardize_data(self, data: List[Dict], source: str, max_items: int) -> List[Dict]:
        """清洗和标准化数据"""
        cleaned_data = []
        
        for item in data[:max_items]:
            try:
                # 提取和清洗名称
                name = self.extract_text_field(item, ['tool_name', 'name', 'title'])
                if not name or len(name.strip()) < 2:
                    continue
                
                # 提取和清洗描述
                description = self.extract_text_field(item, ['description', 'tagline', 'summary'])
                if not description:
                    description = "AI工具描述暂无"
                
                # 提取分类
                categories = self.extract_categories(item)
                
                # 提取链接
                link = self.extract_text_field(item, ['link', 'url', 'href'])
                if link and not link.startswith('http'):
                    # 构建完整URL
                    if source == 'toolify':
                        link = f"https://www.toolify.ai{link}"
                    elif source == 'producthunt':
                        link = f"https://www.producthunt.com{link}"
                    elif source == 'futuretools':
                        link = f"https://www.futuretools.io{link}"
                
                # 创建标准化数据
                standardized_item = {
                    'name': name.strip(),
                    'description': description.strip(),
                    'categories': categories,
                    'link': link,
                    'source': source,
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'pricing': self.extract_text_field(item, ['pricing', 'price', 'cost']),
                    'features': self.extract_list_field(item, ['features', 'capabilities']),
                    'upvotes': self.extract_text_field(item, ['upvotes', 'votes'])
                }
                
                cleaned_data.append(standardized_item)
                
            except Exception as e:
                if self.debug_mode:
                    print(f"⚠️ 清洗数据时出错: {e}")
                continue
        
        return cleaned_data
    
    def extract_text_field(self, item: Dict, field_names: List[str]) -> Optional[str]:
        """提取文本字段"""
        for field_name in field_names:
            if field_name in item:
                value = item[field_name]
                if isinstance(value, str) and value.strip():
                    return value.strip()
                elif isinstance(value, list) and value:
                    return str(value[0]).strip()
        return None
    
    def extract_list_field(self, item: Dict, field_names: List[str]) -> List[str]:
        """提取列表字段"""
        for field_name in field_names:
            if field_name in item:
                value = item[field_name]
                if isinstance(value, list):
                    return [str(v).strip() for v in value if str(v).strip()]
                elif isinstance(value, str) and value.strip():
                    return [value.strip()]
        return []
    
    def extract_categories(self, item: Dict) -> List[str]:
        """提取分类信息"""
        categories = []
        
        # 尝试多个可能的分类字段
        for field_name in ['categories', 'tags', 'category', 'tag']:
            if field_name in item:
                value = item[field_name]
                if isinstance(value, list):
                    for cat in value:
                        if isinstance(cat, dict) and 'category' in cat:
                            categories.append(cat['category'])
                        elif isinstance(cat, str) and cat.strip():
                            categories.append(cat.strip())
                elif isinstance(value, str) and value.strip():
                    categories.append(value.strip())
        
        return categories[:5]  # 限制分类数量
    
    async def scrape_multiple_sites(self, urls_config: Dict[str, Dict], use_llm: bool = False) -> List[Dict]:
        """并发爬取多个站点"""
        all_tools = []
        
        # 创建任务列表
        tasks = []
        for url, config in urls_config.items():
            site_name = config.get('name', 'unknown')
            max_items = config.get('max_items', 50)
            
            if use_llm:
                task = self.scrape_site_with_llm(url, site_name, max_items)
            else:
                task = self.scrape_site_with_css(url, site_name, max_items)
            
            tasks.append(task)
        
        # 并发执行任务
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理结果
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"❌ 任务 {i} 执行失败: {result}")
            else:
                all_tools.extend(result)
        
        # 去重
        unique_tools = self.remove_duplicates(all_tools)
        
        print(f"📊 总共爬取到 {len(unique_tools)} 个独特的AI工具")
        return unique_tools
    
    def remove_duplicates(self, tools: List[Dict]) -> List[Dict]:
        """根据工具名称去重"""
        seen_names = set()
        unique_tools = []
        
        for tool in tools:
            name = tool.get('name', '').lower().strip()
            if name and name not in seen_names:
                seen_names.add(name)
                unique_tools.append(tool)
        
        return unique_tools
    
    async def deep_crawl_site(self, start_url: str, max_pages: int = 10) -> List[Dict]:
        """深度爬取网站（使用BFS策略）"""
        
        crawl_config = CrawlerRunConfig(
            cache_mode=CacheMode.ENABLED,
            output_formats=['markdown', 'links'],
            # 只爬取AI工具相关页面
            include_patterns=[
                r".*/(tool|ai|product|app)/.*",
                r".*/tools/.*",
                r".*/ai-tools/.*"
            ],
            exclude_patterns=[
                r".*/(login|register|contact|about|privacy|terms)/.*",
                r".*/\.(jpg|jpeg|png|gif|pdf|doc|docx)$"
            ],
            scope='domain',
            delay_between_requests=1.0,
            respect_robots_txt=True,
            max_retries=3,
            wait_for_timeout=2000,
        )
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            print(f"🔄 开始深度爬取: {start_url}")
            
            crawl_generator = await crawler.adeep_crawl(
                start_url=start_url,
                strategy="bfs",  # 广度优先搜索
                max_depth=3,
                max_pages=max_pages,
                config=crawl_config
            )
            
            all_tools = []
            page_count = 0
            
            async for result in crawl_generator:
                page_count += 1
                
                if result.success:
                    print(f"[{page_count:02d}] 深度: {result.depth}, URL: {result.url}")
                    
                    # 从markdown内容中提取工具信息
                    # 这里可以使用更复杂的提取逻辑
                    if result.markdown and 'AI' in result.markdown.fit_markdown:
                        # 简单的工具信息提取
                        tool_info = {
                            'name': f"发现的工具_{page_count}",
                            'description': result.markdown.fit_markdown[:200] + "...",
                            'categories': ['AI', 'Tools'],
                            'link': result.url,
                            'source': 'deep_crawl',
                            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'depth': result.depth
                        }
                        all_tools.append(tool_info)
                
                else:
                    print(f"[{page_count:02d}] 失败: {result.url}, 错误: {result.error_message}")
            
            print(f"✅ 深度爬取完成，访问了 {page_count} 个页面，发现 {len(all_tools)} 个工具")
            return all_tools


# 使用示例
async def main():
    """主函数示例"""
    scraper = Crawl4AIScraper(debug_mode=True)
    
    # 配置要爬取的站点
    urls_config = {
        "https://www.toolify.ai/": {
            "name": "toolify",
            "max_items": 30
        },
        "https://www.producthunt.com/topics/artificial-intelligence": {
            "name": "producthunt",
            "max_items": 25
        },
        "https://www.futuretools.io/": {
            "name": "futuretools",
            "max_items": 20
        }
    }
    
    try:
        # 1. 使用CSS选择器策略爬取
        print("🚀 开始使用CSS选择器策略爬取...")
        css_results = await scraper.scrape_multiple_sites(urls_config, use_llm=False)
        
        # 2. 使用LLM策略爬取（可选）
        print("\n🤖 开始使用LLM策略爬取...")
        llm_results = await scraper.scrape_multiple_sites(urls_config, use_llm=True)
        
        # 3. 深度爬取示例
        print("\n🔄 开始深度爬取...")
        deep_results = await scraper.deep_crawl_site("https://www.toolify.ai/", max_pages=5)
        
        # 合并结果
        all_results = css_results + llm_results + deep_results
        unique_results = scraper.remove_duplicates(all_results)
        
        print(f"\n📊 最终结果: {len(unique_results)} 个独特的AI工具")
        
        # 保存结果
        with open('crawl4ai_results.json', 'w', encoding='utf-8') as f:
            json.dump(unique_results, f, ensure_ascii=False, indent=2)
        
        print("✅ 结果已保存到 crawl4ai_results.json")
        
    except Exception as e:
        print(f"❌ 爬取过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main()) 