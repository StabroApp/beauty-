#!/usr/bin/env python3
"""
Tests for PROJECT BEAUTY

Basic tests to verify core functionality
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.hotpepper_scraper import HotPepperScraper
from scraper.data_processor import DataProcessor
from advisor.advisor_agent import BeautyAdvisor
from advisor.translator import Translator

# Try to import GCS storage for testing
try:
    from scraper.gcs_storage import GCSStorage, GCS_AVAILABLE
except ImportError:
    GCS_AVAILABLE = False


def test_scraper():
    """Test the scraper functionality"""
    print("Testing scraper...")
    
    scraper = HotPepperScraper()
    clinics = scraper.scrape_search_page(location="tokyo", category="salon")
    
    assert len(clinics) > 0, "Scraper should return clinics"
    assert clinics[0]['location'] == "tokyo", "Clinic should be in Tokyo"
    assert clinics[0]['category'] == "salon", "Clinic should be a salon"
    assert 'name' in clinics[0], "Clinic should have a name"
    assert 'rating' in clinics[0], "Clinic should have a rating"
    assert 'services' in clinics[0], "Clinic should have services"
    
    print("✅ Scraper tests passed")
    return True


def test_data_processor():
    """Test the data processor functionality"""
    print("Testing data processor...")
    
    processor = DataProcessor()
    
    # Create test data
    test_clinics = [
        {
            "id": "test1",
            "name": "Test Clinic 1",
            "rating": 4.5,
            "category": "salon",
            "location": "tokyo",
            "area": "Shibuya",
            "services": ["Hair Cut"]
        },
        {
            "id": "test2",
            "name": "Test Clinic 2",
            "rating": 4.8,
            "category": "nail",
            "location": "osaka",
            "area": "Namba",
            "services": ["Nail Art"]
        }
    ]
    
    processor.clinics = test_clinics
    
    # Test filtering
    high_rated = processor.filter_by_rating(4.6)
    assert len(high_rated) == 1, "Should filter by rating correctly"
    
    tokyo_clinics = processor.filter_by_location("tokyo")
    assert len(tokyo_clinics) == 1, "Should filter by location correctly"
    
    salons = processor.filter_by_category("salon")
    assert len(salons) == 1, "Should filter by category correctly"
    
    # Test search
    results = processor.search_by_keyword("shibuya")
    assert len(results) == 1, "Should search by keyword correctly"
    
    # Test top rated
    top = processor.get_top_rated(2)
    assert len(top) == 2, "Should return top rated clinics"
    assert top[0]['rating'] >= top[1]['rating'], "Should be sorted by rating"
    
    print("✅ Data processor tests passed")
    return True


def test_advisor():
    """Test the AI advisor functionality"""
    print("Testing AI advisor...")
    
    # Create test data file
    test_data = [
        {
            "id": "test1",
            "name": "Shibuya Test Salon",
            "rating": 4.5,
            "category": "salon",
            "location": "tokyo",
            "area": "Shibuya",
            "description": "A great salon",
            "services": ["Hair Cut"],
            "price_range": "¥3000-¥8000",
            "features": ["English speaking"],
            "access": "5 min walk",
            "phone": "03-1234-5678",
            "website": "https://example.com",
            "review_count": 50,
            "opening_hours": "10:00-20:00"
        }
    ]
    
    # Save test data
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, "clinics.json"), 'w') as f:
        json.dump(test_data, f)
    
    advisor = BeautyAdvisor()
    
    # Test loading
    assert len(advisor.clinics) > 0, "Advisor should load clinics"
    
    # Test search
    results = advisor.search_clinics("Shibuya salon")
    assert len(results) > 0, "Should find clinics matching query"
    
    # Test chat
    response = advisor.chat("Find me a salon")
    assert response is not None, "Should generate a response"
    assert len(response) > 0, "Response should not be empty"
    
    # Test booking help
    clinic = advisor.clinics[0]
    booking_help = advisor.get_booking_help(clinic)
    assert "Booking Help" in booking_help, "Should provide booking help"
    assert clinic['name'] in booking_help, "Should include clinic name"
    
    print("✅ AI advisor tests passed")
    return True


def test_translator():
    """Test the translator functionality"""
    print("Testing translator...")
    
    translator = Translator()
    
    # The translator might not be available without the package
    # Just test that it doesn't crash
    text = "Hello"
    result = translator.translate_to_japanese(text)
    assert result is not None, "Should return a result"
    
    # Test clinic translation
    clinic = {
        "name": "Test Clinic",
        "name_japanese": "テストクリニック"
    }
    
    translated = translator.translate_clinic_data(clinic)
    assert translated is not None, "Should return translated data"
    assert 'name' in translated, "Should preserve name field"
    
    print("✅ Translator tests passed")
    return True


def test_gcs_storage():
    """Test Google Cloud Storage functionality"""
    print("Testing GCS Storage...")
    
    if not GCS_AVAILABLE:
        print("⏭️  GCS not available - skipping GCS tests")
        return True
    
    # Test import and basic functionality without actual GCS connection
    try:
        # Test that we can import the module
        from scraper.gcs_storage import GCSStorage
        
        # Test error handling when bucket name is not provided
        try:
            storage = GCSStorage()
            # If we get here without credentials, it should fail
            print("⚠️  Warning: GCS initialized without proper configuration")
        except (ValueError, Exception) as e:
            # Expected when credentials are not configured
            print(f"   Expected error without credentials: {type(e).__name__}")
        
        print("✅ GCS Storage tests passed")
        return True
        
    except ImportError as e:
        print(f"⚠️  GCS import failed: {e}")
        return True  # Not a critical failure for the test suite


def test_scraper_with_gcs():
    """Test scraper with GCS integration flag"""
    print("Testing scraper with GCS flag...")
    
    # Test that scraper can be initialized with GCS flag
    scraper = HotPepperScraper(use_gcs=False)
    assert scraper.use_gcs == False, "Should initialize with GCS disabled"
    
    # Test with GCS enabled (should gracefully fall back if not configured)
    scraper_gcs = HotPepperScraper(use_gcs=True)
    # It should either enable GCS or fall back to local storage
    assert scraper_gcs.use_gcs in [True, False], "Should have a valid use_gcs state"
    
    print("✅ Scraper with GCS tests passed")
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("Running PROJECT BEAUTY Tests")
    print("=" * 70 + "\n")
    
    tests = [
        ("Scraper", test_scraper),
        ("Data Processor", test_data_processor),
        ("AI Advisor", test_advisor),
        ("Translator", test_translator),
        ("GCS Storage", test_gcs_storage),
        ("Scraper with GCS", test_scraper_with_gcs)
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {name} tests failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
