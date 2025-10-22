#!/usr/bin/env python3
"""
Example Use Cases for PROJECT BEAUTY

This script demonstrates various ways to use the PROJECT BEAUTY system.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper.hotpepper_scraper import HotPepperScraper
from scraper.data_processor import DataProcessor
from advisor.advisor_agent import BeautyAdvisor


def example_1_scrape_multiple_cities():
    """Example 1: Scraping clinics from multiple cities"""
    print("\n" + "=" * 70)
    print("Example 1: Scraping Multiple Cities")
    print("=" * 70 + "\n")
    
    scraper = HotPepperScraper()
    
    cities = ["tokyo", "osaka", "kyoto"]
    categories = ["salon", "nail", "esthetic"]
    
    all_clinics = []
    
    for city in cities:
        for category in categories:
            print(f"Scraping {category} clinics in {city}...")
            clinics = scraper.scrape_search_page(location=city, category=category)
            all_clinics.extend(clinics)
    
    print(f"\n✅ Total clinics scraped: {len(all_clinics)}")
    
    # Save combined data
    scraper.clinics = all_clinics
    scraper.save_to_json("all_clinics.json")


def example_2_find_top_rated():
    """Example 2: Finding top-rated clinics"""
    print("\n" + "=" * 70)
    print("Example 2: Finding Top-Rated Clinics")
    print("=" * 70 + "\n")
    
    processor = DataProcessor()
    clinics = processor.load_clinics()
    
    print("Top 5 Highest-Rated Clinics:\n")
    
    for i, clinic in enumerate(processor.get_top_rated(5), 1):
        print(f"{i}. {clinic['name']}")
        print(f"   ⭐ Rating: {clinic['rating']}/5 ({clinic['review_count']} reviews)")
        print(f"   📍 Location: {clinic['area']}, {clinic['location']}")
        print(f"   💰 Price: {clinic['price_range']}")
        print(f"   🔗 Website: {clinic['website']}\n")


def example_3_search_by_area():
    """Example 3: Searching for clinics in a specific area"""
    print("\n" + "=" * 70)
    print("Example 3: Searching by Area")
    print("=" * 70 + "\n")
    
    processor = DataProcessor()
    clinics = processor.load_clinics()
    
    search_areas = ["Shibuya", "Shinjuku", "Ginza"]
    
    for area in search_areas:
        results = processor.search_by_keyword(area)
        print(f"\nClinics in {area}: {len(results)}")
        for clinic in results[:2]:  # Show first 2
            print(f"  - {clinic['name']} ({clinic['rating']}/5)")


def example_4_filter_by_category():
    """Example 4: Filtering clinics by category"""
    print("\n" + "=" * 70)
    print("Example 4: Filtering by Category")
    print("=" * 70 + "\n")
    
    processor = DataProcessor()
    clinics = processor.load_clinics()
    
    categories = ["salon", "nail", "esthetic", "eyelash"]
    
    for category in categories:
        results = processor.filter_by_category(category)
        if results:
            print(f"\n{category.capitalize()} Clinics: {len(results)}")
            print(f"  Average rating: {sum(c['rating'] for c in results) / len(results):.2f}/5")


def example_5_ai_conversation():
    """Example 5: AI Advisor conversation flow"""
    print("\n" + "=" * 70)
    print("Example 5: AI Advisor Conversation")
    print("=" * 70 + "\n")
    
    advisor = BeautyAdvisor()
    
    # Simulate a conversation
    conversation = [
        "What beauty services are available?",
        "I'm looking for a salon in Tokyo",
        "Show me places with high ratings",
    ]
    
    print("Simulated Conversation:\n")
    
    for i, query in enumerate(conversation, 1):
        print(f"User: {query}")
        response = advisor.chat(query)
        # Print first 200 characters of response
        print(f"Advisor: {response[:200]}...")
        print()


def example_6_booking_workflow():
    """Example 6: Complete booking workflow"""
    print("\n" + "=" * 70)
    print("Example 6: Complete Booking Workflow")
    print("=" * 70 + "\n")
    
    processor = DataProcessor()
    clinics = processor.load_clinics()
    
    advisor = BeautyAdvisor()
    
    # Step 1: Search for clinics
    print("Step 1: Search for clinics in Shibuya")
    results = processor.search_by_keyword("Shibuya")
    
    if results:
        clinic = results[0]
        print(f"✅ Found: {clinic['name']}\n")
        
        # Step 2: Get clinic details
        print("Step 2: Review clinic details")
        print(f"   Rating: {clinic['rating']}/5")
        print(f"   Services: {', '.join(clinic['services'])}")
        print(f"   Price: {clinic['price_range']}\n")
        
        # Step 3: Get booking help
        print("Step 3: Get booking instructions")
        help_text = advisor.get_booking_help(clinic)
        print(help_text[:300] + "...\n")


def example_7_data_analysis():
    """Example 7: Analyzing clinic data"""
    print("\n" + "=" * 70)
    print("Example 7: Data Analysis")
    print("=" * 70 + "\n")
    
    processor = DataProcessor()
    clinics = processor.load_clinics()
    
    stats = processor.get_statistics()
    
    print("📊 Database Statistics:\n")
    print(f"Total Clinics: {stats['total_clinics']}")
    print(f"Average Rating: {stats['average_rating']:.2f}/5\n")
    
    print("Categories Distribution:")
    for cat, count in stats['categories'].items():
        percentage = (count / stats['total_clinics']) * 100
        print(f"  {cat.capitalize()}: {count} ({percentage:.1f}%)")
    
    print("\nLocations Distribution:")
    for loc, count in stats['locations'].items():
        percentage = (count / stats['total_clinics']) * 100
        print(f"  {loc.capitalize()}: {count} ({percentage:.1f}%)")


def example_8_custom_queries():
    """Example 8: Custom query patterns"""
    print("\n" + "=" * 70)
    print("Example 8: Custom Query Patterns")
    print("=" * 70 + "\n")
    
    advisor = BeautyAdvisor()
    
    queries = [
        "Budget-friendly salon in Tokyo",
        "Luxury esthetic clinic",
        "English-speaking staff nail salon",
        "Quick haircut near Shibuya station"
    ]
    
    print("Testing various query patterns:\n")
    
    for query in queries:
        print(f"Query: \"{query}\"")
        results = advisor.search_clinics(query)
        print(f"Results: {len(results)} clinics found\n")


def main():
    """Run all examples"""
    print("\n╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║               PROJECT BEAUTY - Example Use Cases                ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    
    examples = [
        example_2_find_top_rated,
        example_3_search_by_area,
        example_4_filter_by_category,
        example_5_ai_conversation,
        example_6_booking_workflow,
        example_7_data_analysis,
        example_8_custom_queries,
    ]
    
    # Note: Skipping example_1 as it would overwrite the current data
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n❌ Error in {example.__name__}: {e}\n")
    
    print("\n" + "=" * 70)
    print("✨ Examples Complete!")
    print("=" * 70)
    print("\nTo run these examples with your own data:")
    print("1. Run: python scraper/hotpepper_scraper.py --location [city] --category [type]")
    print("2. Run: python examples.py")
    print("\nFor more information, see USAGE.md\n")


if __name__ == "__main__":
    main()
