#!/usr/bin/env python3
"""
Test script for Toolify.ai scraper
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.toolify_scraper import ToolifyScraper
from config import Config

def test_toolify_scraper():
    """Test the Toolify scraper"""
    print("🧪 Testing Toolify.ai scraper...")
    
    # Initialize scraper
    scraper = ToolifyScraper()
    
    # Test URL
    test_url = "https://www.toolify.ai/new"
    
    print(f"📍 Target URL: {test_url}")
    
    try:
        # Test scraping
        tools_data = scraper.scrape(test_url)
        
        if tools_data:
            print(f"✅ Successfully scraped {len(tools_data)} tools")
            
            # Display sample results
            print("\n📋 Sample tools found:")
            for i, tool in enumerate(tools_data[:5], 1):
                print(f"{i}. {tool['name']}")
                print(f"   Description: {tool['description'][:100]}...")
                print(f"   Categories: {', '.join(tool['categories'])}")
                print(f"   Source: {tool['source']}")
                print()
            
            # Save results
            scraper.save_to_json(tools_data, "test_toolify_results.json")
            
            return True
        else:
            print("❌ No tools scraped")
            return False
            
    except Exception as e:
        print(f"❌ Scraping failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Toolify scraper test...")
    
    success = test_toolify_scraper()
    
    if success:
        print("🎉 Toolify scraper test completed successfully!")
    else:
        print("💥 Toolify scraper test failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 