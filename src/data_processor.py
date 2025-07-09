import json
import pandas as pd
import hashlib
from typing import List, Dict, Set, Optional
from datetime import datetime, timedelta
import re
from collections import defaultdict
from config import Config

class DataProcessor:
    """Data processing module for aggregating and deduplicating extracted words"""
    
    def __init__(self):
        self.config = Config()
        self.processed_words = {}
        self.word_history = []
        
    def normalize_word(self, word: str) -> str:
        """Normalize word for comparison"""
        # Convert to lowercase and remove extra spaces
        normalized = word.lower().strip()
        
        # Remove special characters except hyphens and underscores
        normalized = re.sub(r'[^\w\s\-_]', '', normalized)
        
        # Replace multiple spaces with single space
        normalized = re.sub(r'\s+', ' ', normalized)
        
        return normalized
    
    def calculate_word_hash(self, word_data: Dict) -> str:
        """Calculate hash for word data to identify duplicates"""
        # Use normalized word + category for hash
        normalized_word = self.normalize_word(word_data.get('word', ''))
        category = word_data.get('category', '').lower()
        
        hash_string = f"{normalized_word}_{category}"
        return hashlib.md5(hash_string.encode()).hexdigest()
    
    def is_duplicate(self, word_data: Dict) -> bool:
        """Check if word is a duplicate"""
        word_hash = self.calculate_word_hash(word_data)
        return word_hash in self.processed_words
    
    def merge_word_data(self, existing_data: Dict, new_data: Dict) -> Dict:
        """Merge data from duplicate words"""
        merged_data = existing_data.copy()
        
        # Update extraction count
        merged_data['extraction_count'] = merged_data.get('extraction_count', 1) + 1
        
        # Update last seen
        merged_data['last_seen'] = new_data.get('extracted_at', datetime.now().isoformat())
        
        # Merge contexts
        existing_contexts = merged_data.get('contexts', [])
        new_context = new_data.get('context', '')
        if new_context and new_context not in existing_contexts:
            existing_contexts.append(new_context)
            merged_data['contexts'] = existing_contexts
        
        # Update importance if new data has higher importance
        importance_levels = {'low': 1, 'medium': 2, 'high': 3}
        current_importance = merged_data.get('importance', 'medium')
        new_importance = new_data.get('importance', 'medium')
        
        if importance_levels.get(new_importance, 2) > importance_levels.get(current_importance, 2):
            merged_data['importance'] = new_importance
        
        # Update trend potential (take higher value)
        current_trend = merged_data.get('trend_potential', 5)
        new_trend = new_data.get('trend_potential', 5)
        merged_data['trend_potential'] = max(current_trend, new_trend)
        
        # Merge related terms
        existing_related = set(merged_data.get('related_terms', []))
        new_related = set(new_data.get('related_terms', []))
        merged_data['related_terms'] = list(existing_related | new_related)
        
        # Merge target sectors
        existing_sectors = set(merged_data.get('target_sectors', []))
        new_sectors = set(new_data.get('target_sectors', []))
        merged_data['target_sectors'] = list(existing_sectors | new_sectors)
        
        return merged_data
    
    def deduplicate_words(self, words_data: List[Dict]) -> List[Dict]:
        """Remove duplicate words and merge their data"""
        if not words_data:
            return []
        
        print(f"Deduplicating {len(words_data)} words...")
        
        for word_data in words_data:
            word_hash = self.calculate_word_hash(word_data)
            
            if self.is_duplicate(word_data):
                # Merge with existing data
                existing_data = self.processed_words[word_hash]
                merged_data = self.merge_word_data(existing_data, word_data)
                self.processed_words[word_hash] = merged_data
            else:
                # Add as new word
                word_data['word_hash'] = word_hash
                word_data['extraction_count'] = 1
                word_data['first_seen'] = word_data.get('extracted_at', datetime.now().isoformat())
                word_data['last_seen'] = word_data.get('extracted_at', datetime.now().isoformat())
                word_data['contexts'] = [word_data.get('context', '')] if word_data.get('context') else []
                
                self.processed_words[word_hash] = word_data
        
        # Convert back to list
        deduplicated_words = list(self.processed_words.values())
        
        print(f"After deduplication: {len(deduplicated_words)} unique words")
        
        return deduplicated_words
    
    def filter_by_criteria(self, words_data: List[Dict]) -> List[Dict]:
        """Filter words based on various criteria"""
        if not words_data:
            return []
        
        filtered_words = []
        
        for word_data in words_data:
            # Skip very common words
            if self.is_common_word(word_data.get('word', '')):
                continue
            
            # Skip words with very low importance and trend potential
            importance = word_data.get('importance', 'medium')
            trend_potential = word_data.get('trend_potential', 5)
            
            if importance == 'low' and trend_potential < 3:
                continue
            
            # Skip words that are too generic
            if self.is_generic_word(word_data.get('word', '')):
                continue
            
            filtered_words.append(word_data)
        
        print(f"After filtering: {len(filtered_words)} words remain")
        
        return filtered_words
    
    def is_common_word(self, word: str) -> bool:
        """Check if word is too common to be interesting"""
        common_words = {
            'new', 'latest', 'advanced', 'powerful', 'innovative', 'cutting-edge',
            'state-of-the-art', 'revolutionary', 'breakthrough', 'next-generation',
            'enhanced', 'improved', 'optimized', 'efficient', 'effective',
            'comprehensive', 'complete', 'full', 'total', 'ultimate', 'best',
            'top', 'leading', 'premier', 'professional', 'enterprise', 'business',
            'solution', 'solutions', 'platform', 'platforms', 'tool', 'tools',
            'software', 'application', 'app', 'service', 'services', 'system',
            'systems', 'technology', 'technologies', 'framework', 'frameworks'
        }
        
        normalized_word = self.normalize_word(word)
        return normalized_word in common_words
    
    def is_generic_word(self, word: str) -> bool:
        """Check if word is too generic"""
        generic_patterns = [
            r'^v\d+(\.\d+)*$',  # Version numbers like v1.0
            r'^\d+(\.\d+)*$',   # Just numbers
            r'^[a-z]{1,2}$',    # Single or double letters
            r'^(beta|alpha|preview|demo|trial)$',  # Common software terms
        ]
        
        normalized_word = self.normalize_word(word)
        
        for pattern in generic_patterns:
            if re.match(pattern, normalized_word):
                return True
        
        return False
    
    def rank_words(self, words_data: List[Dict]) -> List[Dict]:
        """Rank words by importance and various metrics"""
        if not words_data:
            return []
        
        def calculate_score(word_data: Dict) -> float:
            """Calculate overall score for ranking"""
            score = 0
            
            # Importance weight
            importance_weights = {'low': 1, 'medium': 2, 'high': 3}
            score += importance_weights.get(word_data.get('importance', 'medium'), 2) * 10
            
            # Trend potential weight
            score += word_data.get('trend_potential', 5) * 5
            
            # Business value weight
            business_value_weights = {'low': 1, 'medium': 2, 'high': 3}
            score += business_value_weights.get(word_data.get('business_value', 'medium'), 2) * 8
            
            # Extraction count (how many times it appeared)
            score += word_data.get('extraction_count', 1) * 3
            
            # Emerging term bonus
            if word_data.get('is_emerging', False):
                score += 15
            
            # Recency bonus (newer words get higher score)
            try:
                last_seen = datetime.fromisoformat(word_data.get('last_seen', ''))
                days_ago = (datetime.now() - last_seen).days
                recency_bonus = max(0, 10 - days_ago)
                score += recency_bonus
            except:
                pass
            
            return score
        
        # Add scores and sort
        for word_data in words_data:
            word_data['ranking_score'] = calculate_score(word_data)
        
        ranked_words = sorted(
            words_data,
            key=lambda x: x['ranking_score'],
            reverse=True
        )
        
        return ranked_words
    
    def categorize_words(self, words_data: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize words by type"""
        categories = defaultdict(list)
        
        for word_data in words_data:
            category = word_data.get('category', 'Unknown')
            categories[category].append(word_data)
        
        return dict(categories)
    
    def generate_summary_stats(self, words_data: List[Dict]) -> Dict:
        """Generate summary statistics"""
        if not words_data:
            return {}
        
        total_words = len(words_data)
        categories = self.categorize_words(words_data)
        
        importance_counts = defaultdict(int)
        trend_scores = []
        emerging_count = 0
        
        for word_data in words_data:
            importance_counts[word_data.get('importance', 'medium')] += 1
            trend_scores.append(word_data.get('trend_potential', 5))
            if word_data.get('is_emerging', False):
                emerging_count += 1
        
        avg_trend_score = sum(trend_scores) / len(trend_scores) if trend_scores else 0
        
        return {
            'total_words': total_words,
            'categories': {cat: len(words) for cat, words in categories.items()},
            'importance_distribution': dict(importance_counts),
            'average_trend_score': round(avg_trend_score, 2),
            'emerging_terms_count': emerging_count,
            'top_categories': sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)[:5],
            'processing_timestamp': datetime.now().isoformat()
        }
    
    def load_existing_data(self, filename: str = "processed_words.json") -> List[Dict]:
        """Load existing processed words data"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('words', [])
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error loading existing data: {e}")
            return []
    
    def save_processed_data(self, words_data: List[Dict], summary_stats: Dict, filename: str = "processed_words.json"):
        """Save processed words data"""
        try:
            output_data = {
                'words': words_data,
                'summary': summary_stats,
                'last_updated': datetime.now().isoformat(),
                'total_words': len(words_data)
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"Saved {len(words_data)} processed words to {filename}")
            
        except Exception as e:
            print(f"Error saving processed data: {e}")
    
    def process_extracted_words(self, words_data: List[Dict]) -> Dict:
        """Main processing method"""
        if not words_data:
            return {'words': [], 'summary': {}}
        
        print(f"Processing {len(words_data)} extracted words...")
        
        # Load existing data and merge
        existing_words = self.load_existing_data()
        all_words = existing_words + words_data
        
        # Deduplicate
        deduplicated_words = self.deduplicate_words(all_words)
        
        # Filter by criteria
        filtered_words = self.filter_by_criteria(deduplicated_words)
        
        # Rank words
        ranked_words = self.rank_words(filtered_words)
        
        # Generate summary statistics
        summary_stats = self.generate_summary_stats(ranked_words)
        
        # Save processed data
        self.save_processed_data(ranked_words, summary_stats)
        
        return {
            'words': ranked_words,
            'summary': summary_stats
        }
    
    def export_to_csv(self, words_data: List[Dict], filename: str = "ai_words.csv"):
        """Export words data to CSV for easy analysis"""
        if not words_data:
            return
        
        try:
            # Flatten the data for CSV
            flattened_data = []
            for word_data in words_data:
                flat_data = {
                    'word': word_data.get('word', ''),
                    'category': word_data.get('category', ''),
                    'definition': word_data.get('definition', ''),
                    'importance': word_data.get('importance', ''),
                    'trend_potential': word_data.get('trend_potential', 5),
                    'business_value': word_data.get('business_value', ''),
                    'is_emerging': word_data.get('is_emerging', False),
                    'extraction_count': word_data.get('extraction_count', 1),
                    'ranking_score': word_data.get('ranking_score', 0),
                    'first_seen': word_data.get('first_seen', ''),
                    'last_seen': word_data.get('last_seen', ''),
                    'related_terms': ', '.join(word_data.get('related_terms', [])),
                    'target_sectors': ', '.join(word_data.get('target_sectors', [])),
                    'contexts': ' | '.join(word_data.get('contexts', []))
                }
                flattened_data.append(flat_data)
            
            df = pd.DataFrame(flattened_data)
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Exported {len(words_data)} words to {filename}")
            
        except Exception as e:
            print(f"Error exporting to CSV: {e}")

if __name__ == "__main__":
    # Test the data processor
    processor = DataProcessor()
    
    # Sample test data
    sample_words = [
        {
            'word': 'RAG',
            'category': 'AI Technique',
            'definition': 'Retrieval-Augmented Generation',
            'importance': 'high',
            'trend_potential': 8,
            'extracted_at': datetime.now().isoformat()
        },
        {
            'word': 'MultiModal',
            'category': 'AI Capability',
            'definition': 'AI systems that can process multiple types of data',
            'importance': 'high',
            'trend_potential': 9,
            'extracted_at': datetime.now().isoformat()
        }
    ]
    
    result = processor.process_extracted_words(sample_words)
    print(f"Processed {len(result['words'])} words")
    print(f"Summary: {result['summary']}") 