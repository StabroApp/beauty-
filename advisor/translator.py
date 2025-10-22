"""
Translator Module

Handles translation between Japanese and English
"""

try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False
    print("Warning: deep-translator not available. Translation features will be limited.")


from typing import Optional


class Translator:
    """Translate text between Japanese and English"""
    
    def __init__(self):
        if TRANSLATOR_AVAILABLE:
            try:
                self.ja_to_en = GoogleTranslator(source='ja', target='en')
                self.en_to_ja = GoogleTranslator(source='en', target='ja')
                self.enabled = True
            except Exception as e:
                print(f"Could not initialize translator: {e}")
                self.enabled = False
        else:
            self.enabled = False
    
    def translate_to_english(self, text: str) -> str:
        """
        Translate Japanese text to English
        
        Args:
            text: Japanese text to translate
            
        Returns:
            Translated English text
        """
        if not text or not text.strip():
            return ""
        
        if not self.enabled:
            return text
        
        try:
            translated = self.ja_to_en.translate(text)
            return translated if translated else text
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def translate_to_japanese(self, text: str) -> str:
        """
        Translate English text to Japanese
        
        Args:
            text: English text to translate
            
        Returns:
            Translated Japanese text
        """
        if not text or not text.strip():
            return ""
        
        if not self.enabled:
            return text
        
        try:
            translated = self.en_to_ja.translate(text)
            return translated if translated else text
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def translate_clinic_data(self, clinic: dict) -> dict:
        """
        Translate all Japanese fields in clinic data to English
        
        Args:
            clinic: Dictionary containing clinic information
            
        Returns:
            Clinic dictionary with translated fields
        """
        if not self.enabled:
            return clinic
        
        translated = clinic.copy()
        
        # Fields that might need translation
        fields_to_translate = ['name_japanese', 'description_japanese', 'address_japanese']
        
        for field in fields_to_translate:
            if field in clinic and clinic[field]:
                english_field = field.replace('_japanese', '')
                if english_field not in clinic or not clinic[english_field]:
                    translated[english_field] = self.translate_to_english(clinic[field])
        
        return translated


if __name__ == "__main__":
    translator = Translator()
    
    # Test translation
    japanese_text = "東京にあるプレミアムサロン"
    english_text = translator.translate_to_english(japanese_text)
    print(f"Japanese: {japanese_text}")
    print(f"English: {english_text}")
