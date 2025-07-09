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
        # Initialize OpenAI client with proper API key
        self.client = openai.OpenAI(
            api_key=self.config.OPENAI_API_KEY,
            timeout=30.0,
            max_retries=3
        )
        self.extracted_words = set()
        
    def analyze_tools_batch(self, tools_data: List[Dict]) -> List[Dict]:
        """Analyze a batch of AI tools and extract new words"""
        if not tools_data:
            return []
        
        print(f"Analyzing {len(tools_data)} AI tools with OpenAI...")
        
        # Split tools into batches to avoid token limits
        batch_size = self.config.BATCH_SIZE
        all_new_words = []
        
        for i in range(0, len(tools_data), batch_size):
            batch = tools_data[i:i + batch_size]
            batch_words = self.analyze_single_batch(batch)
            all_new_words.extend(batch_words)
            
            if self.config.DEBUG_MODE:
                print(f"Processed batch {i//batch_size + 1}/{(len(tools_data) + batch_size - 1)//batch_size}")
            
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
                    max_tokens=2000,
                    timeout=30
                )
                
                # Parse the response
                result = response.choices[0].message.content
                new_words = self.parse_openai_response(result)
                
                return new_words
                
            except openai.OpenAIError as e:
                print(f"OpenAI API error: {e}")
                return []
            except Exception as e:
                print(f"Unexpected error calling OpenAI: {e}")
                return []
            
        except Exception as e:
            print(f"Error analyzing batch with OpenAI: {e}")
            return []
    
    def prepare_tools_text(self, tools_batch: List[Dict]) -> str:
        """Prepare tools data for OpenAI analysis"""
        tools_text = ""
        for i, tool in enumerate(tools_batch, 1):
            tools_text += f"{i}. Tool: {tool['name']}\n"
            tools_text += f"   Description: {tool['description']}\n"
            tools_text += f"   Categories: {', '.join(tool.get('categories', []))}\n"
            tools_text += "\n"
        return tools_text
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for OpenAI"""
        return """You are an AI expert specializing in analyzing AI tools and extracting new terminology, concepts, and buzzwords from the AI/tech industry. Your task is to identify:

1. New or emerging AI terms, concepts, and buzzwords
2. Technical terminology that might be trending
3. Product names, technologies, or methodologies mentioned
4. Industry jargon and specialized vocabulary

Focus on terms that are:
- Relatively new or emerging in the AI space
- Technical or specialized terminology
- Trending buzzwords in the industry
- Names of specific AI technologies, models, or methodologies

Avoid common words, generic terms, and well-established vocabulary.

Return your analysis in the following JSON format:
{
  "new_words": [
    {
      "word": "term or phrase",
      "category": "category (e.g., 'AI Model', 'Technology', 'Methodology', 'Buzzword')",
      "definition": "brief definition or explanation",
      "context": "where/how it was mentioned",
      "importance": "high/medium/low"
    }
  ]
}"""
    
    def create_analysis_prompt(self, tools_text: str) -> str:
        """Create the analysis prompt for OpenAI"""
        return f"""Please analyze the following AI tools and extract new words, terms, concepts, and buzzwords:

{tools_text}

Please identify and extract:
1. New or emerging AI terminology
2. Technical buzzwords and jargon
3. Product names and technologies
4. Methodologies and concepts
5. Industry-specific vocabulary

Return the results in the specified JSON format."""
    
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
                print(f"Failed to parse JSON response: {response}")
        
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
    
    def enhance_word_data(self, word_data: Dict) -> Dict:
        """Enhance word data with additional analysis"""
        try:
            word = word_data['word']
            
            # Additional analysis prompt
            enhancement_prompt = f"""Please provide additional analysis for the AI term "{word}":

1. Is this a genuinely new or emerging term in AI?
2. What is its trend potential (1-10)?
3. What industry sectors would be most interested?
4. Any related terms or synonyms?
5. Is it worth tracking for business/investment purposes?

Please respond in JSON format:
{{
  "is_emerging": true/false,
  "trend_potential": 1-10,
  "target_sectors": ["sector1", "sector2"],
  "related_terms": ["term1", "term2"],
  "business_value": "high/medium/low",
  "explanation": "brief explanation"
}}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an AI industry analyst specializing in trend analysis and terminology tracking."},
                    {"role": "user", "content": enhancement_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            
            if json_match:
                enhancement_data = json.loads(json_match.group(0))
                word_data.update(enhancement_data)
            
        except Exception as e:
            if self.config.DEBUG_MODE:
                print(f"Error enhancing word data for '{word_data['word']}': {e}")
        
        return word_data
    
    def filter_and_rank_words(self, words_data: List[Dict]) -> List[Dict]:
        """Filter and rank words by importance and novelty"""
        if not words_data:
            return []
        
        # Remove duplicates based on word
        unique_words = {}
        for word_data in words_data:
            word = word_data['word'].lower()
            if word not in unique_words:
                unique_words[word] = word_data
        
        # Sort by importance and trend potential
        sorted_words = sorted(
            unique_words.values(),
            key=lambda x: (
                x.get('importance', 'medium') == 'high',
                x.get('trend_potential', 5),
                x.get('business_value', 'medium') == 'high'
            ),
            reverse=True
        )
        
        return sorted_words
    
    def analyze_and_extract(self, tools_data: List[Dict]) -> List[Dict]:
        """Main method to analyze tools and extract new words"""
        if not tools_data:
            return []
        
        # Analyze tools in batches
        new_words = self.analyze_tools_batch(tools_data)
        
        # Filter and rank words
        filtered_words = self.filter_and_rank_words(new_words)
        
        # Enhance top words with additional analysis
        enhanced_words = []
        for word_data in filtered_words[:20]:  # Enhance top 20 words
            enhanced_word = self.enhance_word_data(word_data)
            enhanced_words.append(enhanced_word)
        
        # Add remaining words without enhancement
        enhanced_words.extend(filtered_words[20:])
        
        print(f"Extracted {len(enhanced_words)} new words/terms")
        
        return enhanced_words
    
    def save_analysis_results(self, words_data: List[Dict], filename: str = "extracted_words.json"):
        """Save analysis results to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(words_data, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(words_data)} words to {filename}")
        except Exception as e:
            print(f"Error saving analysis results: {e}")

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