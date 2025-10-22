"""
Data Processor

Process and clean scraped beauty clinic data
"""

import json
from typing import List, Dict
import os


class DataProcessor:
    """Process and clean clinic data"""
    
    def __init__(self):
        self.clinics = []
    
    def load_clinics(self, filename: str = "clinics.json") -> List[Dict]:
        """Load clinic data from JSON file"""
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        filepath = os.path.join(data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            self.clinics = json.load(f)
        
        return self.clinics
    
    def filter_by_rating(self, min_rating: float = 4.0) -> List[Dict]:
        """Filter clinics by minimum rating"""
        return [c for c in self.clinics if c.get('rating', 0) >= min_rating]
    
    def filter_by_location(self, location: str) -> List[Dict]:
        """Filter clinics by location"""
        location_lower = location.lower()
        return [c for c in self.clinics 
                if location_lower in c.get('location', '').lower() 
                or location_lower in c.get('area', '').lower()]
    
    def filter_by_category(self, category: str) -> List[Dict]:
        """Filter clinics by category"""
        category_lower = category.lower()
        return [c for c in self.clinics 
                if category_lower in c.get('category', '').lower()]
    
    def get_top_rated(self, n: int = 5) -> List[Dict]:
        """Get top N highest rated clinics"""
        sorted_clinics = sorted(self.clinics, 
                               key=lambda x: x.get('rating', 0), 
                               reverse=True)
        return sorted_clinics[:n]
    
    def search_by_keyword(self, keyword: str) -> List[Dict]:
        """Search clinics by keyword in name or description"""
        keyword_lower = keyword.lower()
        results = []
        
        # Split keyword into individual words for better matching
        keywords = keyword_lower.split()
        
        for clinic in self.clinics:
            searchable_text = ' '.join([
                clinic.get('name', ''),
                clinic.get('description', ''),
                clinic.get('area', ''),
                clinic.get('location', ''),
                clinic.get('category', ''),
                ' '.join(clinic.get('services', []))
            ]).lower()
            
            # Check if any of the keywords match
            if any(kw in searchable_text for kw in keywords):
                results.append(clinic)
        
        return results
    
    def get_statistics(self) -> Dict:
        """Get statistics about the clinics"""
        if not self.clinics:
            return {}
        
        ratings = [c.get('rating', 0) for c in self.clinics]
        categories = {}
        locations = {}
        
        for clinic in self.clinics:
            cat = clinic.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
            
            loc = clinic.get('location', 'Unknown')
            locations[loc] = locations.get(loc, 0) + 1
        
        return {
            'total_clinics': len(self.clinics),
            'average_rating': sum(ratings) / len(ratings) if ratings else 0,
            'categories': categories,
            'locations': locations
        }


if __name__ == "__main__":
    processor = DataProcessor()
    clinics = processor.load_clinics()
    
    if clinics:
        print(f"Loaded {len(clinics)} clinics")
        stats = processor.get_statistics()
        print(f"\nStatistics:")
        print(f"  Total clinics: {stats['total_clinics']}")
        print(f"  Average rating: {stats['average_rating']:.2f}")
        print(f"  Categories: {stats['categories']}")
        print(f"  Locations: {stats['locations']}")
