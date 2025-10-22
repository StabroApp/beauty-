#!/usr/bin/env python3
"""
PROJECT BEAUTY - AI Beauty Advisor

Main CLI interface for the AI Beauty Advisor
"""

import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Note: python-dotenv not installed. Using environment variables directly.")

from advisor.advisor_agent import BeautyAdvisor
from scraper.hotpepper_scraper import HotPepperScraper


def print_banner():
    """Print welcome banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║              🌸  PROJECT BEAUTY  🌸                           ║
    ║                                                               ║
    ║        AI Beauty Advisor for Japanese Clinics                ║
    ║                                                               ║
    ║    "Making Japanese beauty transparent and accessible        ║
    ║                    to the world"                              ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_help():
    """Print help information"""
    help_text = """
    Commands:
      /help     - Show this help message
      /search   - Search for clinics
      /top      - Show top-rated clinics
      /stats    - Show statistics about clinics
      /scrape   - Scrape new clinic data
      /quit     - Exit the program
    
    Or just chat naturally with the AI advisor!
    
    Examples:
      > What are the best beauty salons in Shibuya?
      > I'm looking for a facial treatment
      > Show me nail salons with high ratings
      > How can I book an appointment?
    """
    print(help_text)


def handle_command(command: str, advisor: BeautyAdvisor) -> bool:
    """
    Handle special commands
    
    Args:
        command: Command string
        advisor: BeautyAdvisor instance
        
    Returns:
        True if should continue, False if should exit
    """
    command = command.strip().lower()
    
    if command == '/quit' or command == '/exit':
        print("\n👋 Thank you for using PROJECT BEAUTY! Have a wonderful day!")
        return False
    
    elif command == '/help':
        print_help()
    
    elif command == '/search':
        location = input("📍 Location (e.g., tokyo, osaka): ").strip()
        category = input("💅 Category (salon, nail, eyelash, esthetic): ").strip() or "salon"
        response = advisor.chat(f"Find {category} clinics in {location}")
        print(f"\n🤖 AI Advisor:\n{response}\n")
    
    elif command == '/top':
        top_clinics = advisor.processor.get_top_rated(5)
        print("\n⭐ Top 5 Rated Clinics:\n")
        for i, clinic in enumerate(top_clinics, 1):
            print(f"{i}. {clinic['name']} - {clinic['rating']}/5 ⭐")
            print(f"   📍 {clinic['area']}, {clinic['location']}")
            print(f"   💰 {clinic['price_range']}")
            print()
    
    elif command == '/stats':
        stats = advisor.processor.get_statistics()
        print("\n📊 Clinic Statistics:\n")
        print(f"Total Clinics: {stats['total_clinics']}")
        print(f"Average Rating: {stats['average_rating']:.2f}/5")
        print(f"\nCategories:")
        for cat, count in stats['categories'].items():
            print(f"  - {cat.capitalize()}: {count}")
        print(f"\nLocations:")
        for loc, count in stats['locations'].items():
            print(f"  - {loc.capitalize()}: {count}")
        print()
    
    elif command == '/scrape':
        print("\n🔍 Scraping new clinic data...\n")
        location = input("📍 Location (e.g., tokyo, osaka, kyoto): ").strip() or "tokyo"
        category = input("💅 Category (salon, nail, eyelash, esthetic): ").strip() or "salon"
        
        scraper = HotPepperScraper()
        clinics = scraper.scrape_search_page(location=location, category=category)
        scraper.save_to_json()
        
        print(f"\n✅ Scraped {len(clinics)} clinics!")
        print("Reloading data...")
        
        # Reload clinics in advisor
        advisor.clinics = advisor.processor.load_clinics()
        advisor.vector_store.create_from_clinics(advisor.clinics)
        
        print("✅ Data updated!\n")
    
    else:
        print(f"Unknown command: {command}")
        print("Type /help for available commands\n")
    
    return True


def main():
    """Main function"""
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables.")
        print("   The AI advisor will run in limited mode without AI features.")
        print("   To enable full features, add your API key to a .env file.\n")
    
    # Initialize advisor
    print("Initializing AI Beauty Advisor...")
    advisor = BeautyAdvisor(api_key=api_key)
    
    # Check if we have clinic data
    if not advisor.clinics:
        print("\n⚠️  No clinic data found!")
        print("   Let's scrape some data first...\n")
        
        location = input("📍 Location (default: tokyo): ").strip() or "tokyo"
        category = input("💅 Category (default: salon): ").strip() or "salon"
        
        scraper = HotPepperScraper()
        clinics = scraper.scrape_search_page(location=location, category=category)
        scraper.save_to_json()
        
        advisor.clinics = advisor.processor.load_clinics()
        advisor.vector_store.create_from_clinics(advisor.clinics)
        
        print(f"\n✅ Loaded {len(advisor.clinics)} clinics!\n")
    
    # Print banner and welcome
    print_banner()
    print(f"✨ Loaded {len(advisor.clinics)} beauty clinics")
    print("\nType /help for commands or just start chatting!\n")
    
    # Main conversation loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith('/'):
                if not handle_command(user_input, advisor):
                    break
                continue
            
            # Chat with advisor
            print("\n🤖 AI Advisor:")
            response = advisor.chat(user_input)
            print(f"{response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using PROJECT BEAUTY! Have a wonderful day!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
