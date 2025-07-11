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
        return """你是一个AI专家，专门分析AI工具并从AI/技术行业中提取新术语、概念和流行语。你的任务是识别：

1. 新的或新兴的AI术语、概念和流行语
2. 可能正在流行的技术术语
3. 提到的产品名称、技术或方法
4. 行业术语和专业词汇

重点关注以下术语：
- 在AI领域相对较新或新兴的
- 技术性或专业术语
- 行业中的流行词汇
- 特定AI技术、模型或方法的名称

避免常见词汇、通用术语和已确立的词汇。

请以下列JSON格式返回分析结果：
{
  "new_words": [
    {
      "word": "术语或短语",
      "category": "类别 (例如：'AI模型', '技术', '方法', '流行语')",
      "definition": "简短定义或解释",
      "context": "在哪里/如何提到的",
      "importance": "high/medium/low"
    }
  ]
}"""
    
    def create_analysis_prompt(self, tools_text: str) -> str:
        """Create the analysis prompt for OpenAI"""
        return f"""请分析以下AI工具并提取新词汇、术语、概念和流行语：

{tools_text}

请识别并提取：
1. 新的或新兴的AI术语
2. 技术流行语和术语
3. 产品名称和技术
4. 方法和概念
5. 行业专用词汇

请按照指定的JSON格式返回结果。"""
    
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
        
        # Skip common stop words
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'ai', 'artificial', 'intelligence', 'machine', 'learning', 'deep', 'neural',
            'network', 'model', 'algorithm', 'data', 'tool', 'software', 'platform',
            'solution', 'system', 'technology', 'application', 'service', 'api'
        }
        
        if word in stop_words:
            return False
        
        # Skip very short words (less than 3 characters)
        if len(word) < 3:
            return False
        
        # Add to extracted words set
        self.extracted_words.add(word)
        
        return True
    
    def filter_and_rank_words(self, words_data: List[Dict]) -> List[Dict]:
        """Filter and rank words by importance and novelty"""
        if not words_data:
            return []
        
        # Filter out duplicates and low-quality words
        unique_words = {}
        for word_data in words_data:
            word = word_data['word'].lower()
            if word not in unique_words:
                unique_words[word] = word_data
        
        # Convert back to list and sort by importance
        filtered_words = list(unique_words.values())
        
        # Sort by importance (high > medium > low)
        importance_order = {'high': 3, 'medium': 2, 'low': 1}
        filtered_words.sort(
            key=lambda x: importance_order.get(x.get('importance', 'medium'), 2),
            reverse=True
        )
        
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