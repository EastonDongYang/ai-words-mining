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
        return """You are an expert in discovering trending English keywords from AI/technology content. Your goal is to identify commercial-viable terms suitable for Google Trends analysis and website building.

⚠️ IMPORTANT - Focus on these types of terms:
- NEW product names or features that emerged in the last 7-15 days
- TRENDING commercial keywords with high search volume
- SPECIFIC application names, tool names, or service names
- VIRAL technology terms and buzzwords
- COMMERCIAL phrases that people actively search for

✅ PRIORITIZE extracting:
1. **New Product/Service Names**: Recently launched AI tools, features, or services
2. **Commercial Keywords**: Terms with high commercial and search value
3. **Trending Phrases**: Viral terms spreading across social media and tech communities
4. **Application-Specific Terms**: Specific use cases, workflows, or applications
5. **Marketing Buzzwords**: Terms used in marketing and business contexts

🎯 Evaluation Criteria:
- Commercial Value: Can be monetized through websites/affiliate marketing
- Search Volume: High potential for Google Trends and search traffic
- Recency: Appeared or became popular within the last 7-15 days
- Viral Potential: Likely to be shared and searched by users
- Business Application: Can build a profitable website around this term

🚫 AVOID these academic/conceptual terms:
- Broad academic concepts (e.g., "Edge AI Deployment", "Privacy-Preserving ML")
- Generic technology terms (e.g., "Machine Learning", "Deep Learning")
- Overly technical jargon without commercial appeal
- Established academic terminology

Return results ONLY in English using this JSON format:
{
  "new_words": [
    {
      "word": "Specific product name, feature, or commercial term",
      "category": "Category (e.g., 'New Product', 'Trending Feature', 'Commercial Tool', 'Viral Term')",
      "definition": "Brief commercial description and what it does",
      "context": "How it appears in the description",
      "importance": "high/medium/low",
      "trend_potential": "1-10 score for Google Trends search potential",
      "business_value": "high/medium/low for monetization potential",
      "is_emerging": "true/false for whether it's newly emerged (7-15 days)",
      "search_volume_estimate": "high/medium/low estimated search volume",
      "commercial_appeal": "high/medium/low for building websites/affiliate marketing"
    }
  ]
}"""
    
    def create_analysis_prompt(self, tools_text: str) -> str:
        """Create the analysis prompt for OpenAI"""
        return f"""Analyze the following AI tool descriptions and identify TRENDING, COMMERCIAL English keywords that appeared or became popular in the last 7-15 days. Focus on extracting terms with high search volume and commercial value:

{tools_text}

🔍 ANALYSIS FOCUS:
1. Extract NEW product names, features, or services mentioned
2. Identify TRENDING commercial keywords and phrases
3. Find SPECIFIC application names or tool names
4. Discover VIRAL terms with high search potential
5. Focus on terms suitable for Google Trends analysis and website building

⚠️ EXTRACTION STRATEGY:
- Look for specific product names, even if they're new versions of existing tools
- Extract feature names, service names, and application-specific terms
- Focus on terms that people would actively search for
- Prioritize commercial and monetizable keywords
- Include trending buzzwords and marketing terms

✅ GOOD EXAMPLES of what to extract:
- "Claude 3.5 Sonnet" (specific model name)
- "AI Video Generator" (searchable commercial term)
- "Prompt Engineering Tool" (commercial application)
- "No-Code AI Builder" (trending business term)
- "AI Avatar Creator" (specific commercial service)

🚫 AVOID extracting:
- Generic academic concepts
- Broad technology categories
- Overly technical jargon
- Established computer science terms

Return results in the specified JSON format. Each term should have HIGH commercial value, search potential, and be suitable for building profitable websites. RESPOND ONLY IN ENGLISH."""
    
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
                                'search_volume_estimate': word_data.get('search_volume_estimate', 'medium'),
                                'commercial_appeal': word_data.get('commercial_appeal', 'medium'),
                                'extracted_at': time.strftime('%Y-%m-%d %H:%M:%S')
                            })
            
        except json.JSONDecodeError:
            if self.config.DEBUG_MODE:
                print(f"无法解析JSON响应: {response}")
        
        return new_words
    
    def is_valid_word(self, word_data: Dict) -> bool:
        """Validate if a word is worth including - focusing on commercial value"""
        word = word_data.get('word', '').strip().lower()
        
        # Skip empty words
        if not word:
            return False
        
        # Skip if already extracted
        if word in self.extracted_words:
            return False
        
        # Skip very short words (less than 3 characters)
        if len(word) < 3:
            return False
        
        # Skip common stop words but allow commercial terms
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'
        }
        
        if word in stop_words:
            return False
        
        # Priority filters based on commercial value
        trend_potential = word_data.get('trend_potential', 5)
        business_value = word_data.get('business_value', 'medium')
        search_volume = word_data.get('search_volume_estimate', 'medium')
        commercial_appeal = word_data.get('commercial_appeal', 'medium')
        is_emerging = word_data.get('is_emerging', False)
        
        # Calculate a commercial score
        commercial_score = 0
        
        # Trend potential scoring (40% weight)
        if trend_potential >= 8:
            commercial_score += 40
        elif trend_potential >= 6:
            commercial_score += 30
        elif trend_potential >= 4:
            commercial_score += 20
        else:
            return False  # Skip low trend potential
        
        # Business value scoring (30% weight)
        if business_value == 'high':
            commercial_score += 30
        elif business_value == 'medium':
            commercial_score += 20
        else:
            commercial_score += 10
        
        # Search volume scoring (20% weight)
        if search_volume == 'high':
            commercial_score += 20
        elif search_volume == 'medium':
            commercial_score += 15
        else:
            commercial_score += 10
        
        # Commercial appeal scoring (10% weight)
        if commercial_appeal == 'high':
            commercial_score += 10
        elif commercial_appeal == 'medium':
            commercial_score += 7
        else:
            commercial_score += 3
        
        # Emerging bonus
        if is_emerging:
            commercial_score += 15
        
        # Only accept words with good commercial potential
        if commercial_score < 60:
            return False
        
        # Add to extracted words set
        self.extracted_words.add(word)
        
        return True
    
    def filter_and_rank_words(self, words_data: List[Dict]) -> List[Dict]:
        """Filter and rank words by commercial value and trend potential"""
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
        
        # Calculate commercial ranking score for each word
        for word_data in filtered_words:
            score = 0
            
            # Trend potential (35% weight)
            trend_potential = word_data.get('trend_potential', 5)
            score += trend_potential * 3.5
            
            # Business value (25% weight)
            business_value_weights = {'high': 25, 'medium': 15, 'low': 5}
            score += business_value_weights.get(word_data.get('business_value', 'medium'), 15)
            
            # Search volume estimate (25% weight)
            search_volume_weights = {'high': 25, 'medium': 15, 'low': 5}
            score += search_volume_weights.get(word_data.get('search_volume_estimate', 'medium'), 15)
            
            # Commercial appeal (10% weight)
            commercial_appeal_weights = {'high': 10, 'medium': 7, 'low': 3}
            score += commercial_appeal_weights.get(word_data.get('commercial_appeal', 'medium'), 7)
            
            # Emerging concept bonus (5% weight)
            if word_data.get('is_emerging', False):
                score += 5
            
            word_data['ranking_score'] = score
        
        # Sort by ranking score (descending)
        filtered_words.sort(key=lambda x: x.get('ranking_score', 0), reverse=True)
        
        # Take top results based on commercial potential
        top_words = []
        for word_data in filtered_words:
            if word_data.get('ranking_score', 0) >= 50:  # Only high-scoring commercial terms
                top_words.append(word_data)
        
        return top_words
    
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