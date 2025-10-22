#!/usr/bin/env python3
"""
Demo script to showcase PROJECT BEAUTY functionality
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from advisor.advisor_agent import BeautyAdvisor
from scraper.data_processor import DataProcessor
from scraper.hotpepper_scraper import HotPepperScraper


def demo_scraper():
    """Demonstrate the scraper functionality"""
    print("=" * 70)
    print("DEMO 1: Web Scraper")
    print("=" * 70)
    print("\n1. Scraping clinic data from different locations...\n")
    
    # Scrape Tokyo salons
    scraper = HotPepperScraper()
    clinics = scraper.scrape_search_page(location="tokyo", category="salon")
    print(f"\n✅ Scraped {len(clinics)} salons in Tokyo")
    
    # Scrape Osaka nail salons
    clinics = scraper.scrape_search_page(location="osaka", category="nail")
    print(f"✅ Scraped {len(clinics)} nail salons in Osaka")
    
    # Scrape Kyoto esthetic clinics
    clinics = scraper.scrape_search_page(location="kyoto", category="esthetic")
    print(f"✅ Scraped {len(clinics)} esthetic clinics in Kyoto")
    
    print("\nSample clinic data:")
    print(f"  Name: {clinics[0]['name']}")
    print(f"  Location: {clinics[0]['area']}, {clinics[0]['location']}")
    print(f"  Rating: {clinics[0]['rating']}/5 ⭐ ({clinics[0]['review_count']} reviews)")
    print(f"  Services: {', '.join(clinics[0]['services'])}")
    print(f"  Price Range: {clinics[0]['price_range']}")


def demo_data_processing():
    """Demonstrate data processing capabilities"""
    print("\n\n" + "=" * 70)
    print("DEMO 2: Data Processing & Search")
    print("=" * 70)
    
    processor = DataProcessor()
    clinics = processor.load_clinics()
    
    print(f"\n2. Loading and analyzing clinic data...\n")
    print(f"✅ Loaded {len(clinics)} clinics from database")
    
    # Statistics
    stats = processor.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"   Average Rating: {stats['average_rating']:.2f}/5")
    print(f"   Categories: {', '.join(stats['categories'].keys())}")
    print(f"   Locations: {', '.join(stats['locations'].keys())}")
    
    # Top rated
    print(f"\n⭐ Top 3 Rated Clinics:")
    for i, clinic in enumerate(processor.get_top_rated(3), 1):
        print(f"   {i}. {clinic['name']} - {clinic['rating']}/5")
    
    # Search by keyword
    print(f"\n🔍 Searching for 'Shibuya':")
    results = processor.search_by_keyword("Shibuya")
    for clinic in results:
        print(f"   - {clinic['name']} ({clinic['area']})")


def demo_ai_advisor():
    """Demonstrate AI advisor capabilities"""
    print("\n\n" + "=" * 70)
    print("DEMO 3: AI Beauty Advisor")
    print("=" * 70)
    
    print("\n3. Testing AI Beauty Advisor...\n")
    
    advisor = BeautyAdvisor()
    
    # Test queries
    queries = [
        "What are the best salons in Tokyo?",
        "Find me clinics in Shibuya",
        "I'm looking for high-rated places"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n💬 Query {i}: '{query}'")
        print("-" * 70)
        response = advisor.chat(query)
        print(f"🤖 Response:\n{response}")


def demo_booking_help():
    """Demonstrate booking assistance"""
    print("\n\n" + "=" * 70)
    print("DEMO 4: Booking Assistance")
    print("=" * 70)
    
    print("\n4. Getting booking help for a clinic...\n")
    
    processor = DataProcessor()
    clinics = processor.load_clinics()
    
    if clinics:
        advisor = BeautyAdvisor()
        clinic = clinics[0]
        
        print(f"📍 Selected Clinic: {clinic['name']}")
        help_text = advisor.get_booking_help(clinic)
        print(help_text)


def main():
    """Run all demos"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║                   PROJECT BEAUTY DEMO                            ║")
    print("║                                                                  ║")
    print("║           AI Beauty Advisor for Japanese Clinics                ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    
    try:
        demo_scraper()
        demo_data_processing()
        demo_ai_advisor()
        demo_booking_help()
        
        print("\n\n" + "=" * 70)
        print("✨ DEMO COMPLETE!")
        print("=" * 70)
        print("\n💡 To start the interactive AI advisor, run:")
        print("   python beauty_advisor.py\n")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
