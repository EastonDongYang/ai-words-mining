import openai
import json
import time
from typing import List, Dict, Set, Optional
from config import Config
import re

class OpenAIAnalyzer:
    """OpenAI API integration for analyzing AI tools and extracting new words"""
    
    def __init__(self):
        self.config = Config()
        # Initialize OpenAI client with minimal configuration
        self.client = openai.OpenAI(
            api_key=self.config.OPENAI_API_KEY
        )
        self.extracted_words = set()
        
    def analyze_tools_batch(self, tools_data: List[Dict]) -> List[Dict]:
        """Analyze a batch of AI tools and extract new words"""
        if not tools_data:
            return []
        
        print(f"正在使用OpenAI分析 {len(tools_data)} 个AI工具...")
        
        # Split tools into batches to avoid token limits
        batch_size = self.config.BATCH_SIZE
        all_new_words = []
        
        for i in range(0, len(tools_data), batch_size):
            batch = tools_data[i:i + batch_size]
            batch_words = self.analyze_single_batch(batch)
            all_new_words.extend(batch_words)
            
            if self.config.DEBUG_MODE:
                print(f"已处理批次 {i//batch_size + 1}/{(len(tools_data) + batch_size - 1)//batch_size}")
            
            # Add delay between batches to respect rate limits
            time.sleep(1)
        
        return all_new_words
    
    def analyze_single_batch(self, tools_batch: List[Dict]) -> List[Dict]:
        """Analyze a single batch of tools"""
        try:
            # Prepare the data for analysis
            tools_text = self.prepare_tools_text(tools_batch)
            
            # Create the prompt for OpenAI
            prompt = self.create_analysis_prompt(tools_text)
            
            # Call OpenAI API with proper error handling
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": self.get_system_prompt()},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=2000
                )
                
                # Parse the response
                result = response.choices[0].message.content
                new_words = self.parse_openai_response(result)
                
                return new_words
                
            except openai.OpenAIError as e:
                print(f"OpenAI API错误: {e}")
                return []
            except Exception as e:
                print(f"调用OpenAI时发生意外错误: {e}")
                return []
            
        except Exception as e:
            print(f"使用OpenAI分析批次时发生错误: {e}")
            return []
    
    def prepare_tools_text(self, tools_batch: List[Dict]) -> str:
        """Prepare tools data for OpenAI analysis"""
        tools_text = ""
        for i, tool in enumerate(tools_batch, 1):
            tools_text += f"{i}. 工具: {tool['name']}\n"
            tools_text += f"   描述: {tool['description']}\n"
            tools_text += f"   类别: {', '.join(tool.get('categories', []))}\n"
            tools_text += "\n"
        return tools_text
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for OpenAI"""
        return """你是一个新词发现专家，专门从AI/技术内容中发现真正的新兴概念和术语。你的目标是找到适合Google Trends分析和建新词网站的概念性词汇。

⚠️ 重要：请严格避免以下内容：
- 公司名称（如OpenAI、Google、Microsoft等）
- 具体产品名称（如ChatGPT、Claude、Midjourney等）
- 软件工具名称（如LangChain、Hugging Face等）
- 已确立的技术术语（如深度学习、神经网络、机器学习等）
- 版本号和型号（如GPT-4、V6等）

✅ 重点识别以下类型的新兴概念：
1. **新兴技术概念**：最近2年内出现的技术现象和方法论
2. **行业新术语**：AI领域内正在形成的概念性词汇
3. **技术趋势词汇**：描述新技术发展方向的概念
4. **应用场景新词**：新的应用领域和使用方式
5. **方法论新词**：新的工作流程、方法或框架概念

🎯 评估标准：
- 概念性：是概念而非产品
- 新颖性：2年内出现或流行
- 搜索价值：适合Google Trends分析
- 建站价值：可以围绕此概念建立网站
- 趋势性：有增长和传播潜力

请以下列JSON格式返回分析结果：
{
  "new_words": [
    {
      "word": "概念性词汇或术语",
      "category": "类别 (如：'新兴技术', '应用概念', '方法论', '行业趋势')",
      "definition": "概念的详细定义和含义",
      "context": "在描述中的具体体现",
      "importance": "high/medium/low",
      "trend_potential": "1-10分，评估Google Trends搜索潜力",
      "business_value": "high/medium/low，评估建站商业价值",
      "is_emerging": "true/false，是否为新兴概念"
    }
  ]
}"""
    
    def create_analysis_prompt(self, tools_text: str) -> str:
        """Create the analysis prompt for OpenAI"""
        return f"""请分析以下AI工具描述，从中识别新兴概念和技术术语。请忽略具体的产品名称，专注于发现概念性词汇：

{tools_text}

🔍 分析重点：
1. 从工具描述中识别新兴技术概念（而非工具名称）
2. 发现新的应用场景和使用方式
3. 提取描述新技术方法的概念性词汇
4. 识别正在形成的行业新术语
5. 寻找具有Google Trends搜索价值的概念

⚠️ 请严格避免：
- 不要提取具体的产品名称或工具名称
- 不要包含公司名称或品牌
- 不要提取已确立的技术术语
- 不要包含版本号或型号

✅ 专注提取：
- 新兴技术概念和现象
- 应用场景的新术语
- 方法论相关的概念
- 行业发展趋势词汇

请按照指定的JSON格式返回结果，每个词汇都应该是概念性的，适合Google Trends分析和建站使用。"""
    
    def parse_openai_response(self, response: str) -> List[Dict]:
        """Parse OpenAI response and extract new words"""
        new_words = []
        
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
                
                if 'new_words' in data:
                    for word_data in data['new_words']:
                        if self.is_valid_word(word_data):
                            new_words.append({
                                'word': word_data.get('word', '').strip(),
                                'category': word_data.get('category', 'Unknown'),
                                'definition': word_data.get('definition', ''),
                                'context': word_data.get('context', ''),
                                'importance': word_data.get('importance', 'medium'),
                                'trend_potential': word_data.get('trend_potential', 5),
                                'business_value': word_data.get('business_value', 'medium'),
                                'is_emerging': word_data.get('is_emerging', False),
                                'extracted_at': time.strftime('%Y-%m-%d %H:%M:%S')
                            })
            
        except json.JSONDecodeError:
            if self.config.DEBUG_MODE:
                print(f"无法解析JSON响应: {response}")
        
        return new_words
    
    def is_valid_word(self, word_data: Dict) -> bool:
        """Validate if a word is worth including"""
        word = word_data.get('word', '').strip().lower()
        
        # Skip empty words
        if not word:
            return False
        
        # Skip if already extracted
        if word in self.extracted_words:
            return False
        
        # Skip common stop words and established terms
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'ai', 'artificial', 'intelligence', 'machine', 'learning', 'deep', 'neural',
            'network', 'model', 'algorithm', 'data', 'tool', 'software', 'platform',
            'solution', 'system', 'technology', 'application', 'service', 'api'
        }
        
        if word in stop_words:
            return False
        
        # Skip known product names and tools
        product_names = {
            'chatgpt', 'claude', 'midjourney', 'dall-e', 'stable diffusion', 'gpt-4', 'gpt-3',
            'openai', 'anthropic', 'google', 'microsoft', 'hugging face', 'langchain',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'jupyter', 'github',
            'discord', 'slack', 'notion', 'figma', 'canva', 'photoshop', 'premiere',
            'after effects', 'blender', 'unity', 'unreal', 'chrome', 'firefox', 'safari'
        }
        
        if word in product_names:
            return False
        
        # Skip words with version numbers or model numbers
        if re.search(r'[v]\d+', word) or re.search(r'gpt-\d+', word):
            return False
        
        # Skip very short words (less than 3 characters)
        if len(word) < 3:
            return False
        
        # Skip words that are clearly product names (contain version info or brand indicators)
        if any(indicator in word for indicator in ['xl', 'pro', 'plus', 'beta', 'alpha', 'v1', 'v2']):
            return False
        
        # Prefer words that indicate they are emerging concepts
        trend_potential = word_data.get('trend_potential', 5)
        is_emerging = word_data.get('is_emerging', False)
        
        # Skip if trend potential is too low
        if trend_potential < 4:
            return False
        
        # Add to extracted words set
        self.extracted_words.add(word)
        
        return True
    
    def filter_and_rank_words(self, words_data: List[Dict]) -> List[Dict]:
        """Filter and rank words by importance, trend potential, and business value"""
        if not words_data:
            return []
        
        # Filter out duplicates and low-quality words
        unique_words = {}
        for word_data in words_data:
            word = word_data['word'].lower()
            if word not in unique_words:
                unique_words[word] = word_data
        
        # Convert back to list
        filtered_words = list(unique_words.values())
        
        # Calculate ranking score for each word
        for word_data in filtered_words:
            score = 0
            
            # Importance weight (30%)
            importance_weights = {'high': 3, 'medium': 2, 'low': 1}
            score += importance_weights.get(word_data.get('importance', 'medium'), 2) * 30
            
            # Trend potential weight (40%)
            trend_potential = word_data.get('trend_potential', 5)
            score += trend_potential * 4
            
            # Business value weight (20%)
            business_value_weights = {'high': 3, 'medium': 2, 'low': 1}
            score += business_value_weights.get(word_data.get('business_value', 'medium'), 2) * 20
            
            # Emerging concept bonus (10%)
            if word_data.get('is_emerging', False):
                score += 10
            
            word_data['ranking_score'] = score
        
        # Sort by ranking score (descending)
        filtered_words.sort(key=lambda x: x.get('ranking_score', 0), reverse=True)
        
        return filtered_words
    
    def analyze_and_extract(self, tools_data: List[Dict]) -> List[Dict]:
        """Main method to analyze tools and extract new words"""
        if not tools_data:
            print("没有工具数据需要分析")
            return []
        
        # Analyze tools in batches
        all_words = self.analyze_tools_batch(tools_data)
        
        if not all_words:
            print("没有提取到新词汇")
            return []
        
        # Filter and rank the extracted words
        filtered_words = self.filter_and_rank_words(all_words)
        
        print(f"成功提取了 {len(filtered_words)} 个新词汇")
        
        return filtered_words
    
    def save_analysis_results(self, words_data: List[Dict], filename: str = "extracted_words.json"):
        """Save analysis results to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(words_data, f, ensure_ascii=False, indent=2)
            print(f"分析结果已保存到 {filename}")
        except Exception as e:
            print(f"保存分析结果时发生错误: {e}")

if __name__ == "__main__":
    # Test the analyzer
    analyzer = OpenAIAnalyzer()
    
    # Sample test data
    sample_tools = [
        {
            "name": "GPT-4 Turbo",
            "description": "Advanced large language model with multimodal capabilities",
            "categories": ["LLM", "Multimodal AI"]
        },
        {
            "name": "DALL-E 3",
            "description": "Text-to-image generation with improved prompt adherence",
            "categories": ["Image Generation", "Creative AI"]
        }
    ]
    
    results = analyzer.analyze_and_extract(sample_tools)
    analyzer.save_analysis_results(results) 