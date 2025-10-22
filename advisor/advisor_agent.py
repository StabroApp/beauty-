"""
AI Beauty Advisor Agent

Main agent for the AI Beauty Advisor chatbot
"""

import os
import json
from typing import List, Dict, Optional
try:
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("Warning: LangChain not available. Using fallback mode.")

from advisor.translator import Translator
from advisor.vector_store import VectorStore
from scraper.data_processor import DataProcessor


class BeautyAdvisor:
    """AI-powered beauty clinic advisor"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.translator = Translator()
        self.processor = DataProcessor()
        self.vector_store = VectorStore()
        
        # Load clinic data
        self.clinics = self.processor.load_clinics()
        
        if LANGCHAIN_AVAILABLE and self.api_key:
            try:
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.7,
                    openai_api_key=self.api_key
                )
            except Exception as e:
                print(f"Error initializing LLM: {e}")
                self.llm = None
        else:
            self.llm = None
        
        # Try to load existing vector store
        if not self.vector_store.load_existing() and self.clinics:
            self.vector_store.create_from_clinics(self.clinics)
        
        self.conversation_history = []
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the AI advisor"""
        return """You are an AI Beauty Advisor specializing in Japanese beauty clinics. 
Your role is to help international travelers find, compare, and book beauty treatments in Japan.

You have access to information about beauty clinics including:
- Names, locations, and contact information
- Services offered and price ranges
- Customer ratings and reviews
- Accessibility and features

Guidelines:
1. Be friendly, professional, and helpful
2. Provide clear, accurate information about clinics
3. Help users understand their options
4. Guide them through the booking process
5. Explain any Japanese beauty culture or terminology
6. Always translate Japanese terms to English
7. Give personalized recommendations based on user preferences

When users ask about clinics, search the database and provide detailed, relevant information.
If you're not sure about something, be honest and suggest alternatives.
"""
    
    def search_clinics(self, query: str) -> List[Dict]:
        """
        Search for clinics based on user query
        
        Args:
            query: User's search query
            
        Returns:
            List of relevant clinics
        """
        # Use vector store for semantic search if available
        if self.vector_store.vectorstore:
            return self.vector_store.search(query, k=5)
        
        # Fallback to keyword search
        return self.processor.search_by_keyword(query)
    
    def format_clinic_info(self, clinic: Dict) -> str:
        """Format clinic information for display"""
        info = f"""
📍 **{clinic['name']}**
   Category: {clinic.get('category', 'N/A').capitalize()}
   Location: {clinic.get('area', '')}, {clinic.get('location', '').capitalize()}
   Rating: {'⭐' * int(clinic.get('rating', 0))} {clinic.get('rating', 'N/A')}/5 ({clinic.get('review_count', 0)} reviews)
   
   Services: {', '.join(clinic.get('services', []))}
   Price Range: {clinic.get('price_range', 'N/A')}
   
   {clinic.get('description', '')}
   
   Features: {', '.join(clinic.get('features', []))}
   Access: {clinic.get('access', '')}
   Phone: {clinic.get('phone', 'N/A')}
   Website: {clinic.get('website', 'N/A')}
"""
        return info
    
    def chat(self, user_message: str) -> str:
        """
        Process user message and generate response
        
        Args:
            user_message: User's message
            
        Returns:
            AI advisor's response
        """
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Detect if user is asking about specific clinics
        search_keywords = ['find', 'search', 'looking for', 'recommend', 'best', 'clinic', 'salon']
        should_search = any(keyword in user_message.lower() for keyword in search_keywords)
        
        clinic_context = ""
        if should_search:
            clinics = self.search_clinics(user_message)
            if clinics:
                clinic_context = "\n\nRelevant clinics:\n"
                for clinic in clinics[:3]:
                    clinic_context += self.format_clinic_info(clinic)
        
        # Generate response using LLM if available
        if self.llm and LANGCHAIN_AVAILABLE:
            try:
                messages = [
                    SystemMessage(content=self.get_system_prompt()),
                ]
                
                # Add conversation history
                for msg in self.conversation_history[-5:]:  # Last 5 messages
                    messages.append(HumanMessage(content=msg["content"]))
                
                # Add clinic context if available
                if clinic_context:
                    messages.append(SystemMessage(content=f"Here is relevant clinic information:{clinic_context}"))
                
                response = self.llm.invoke(messages)
                assistant_message = response.content
            except Exception as e:
                print(f"Error calling LLM: {e}")
                assistant_message = self._generate_fallback_response(user_message, clinic_context)
        else:
            assistant_message = self._generate_fallback_response(user_message, clinic_context)
        
        # Add to conversation history
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message
    
    def _generate_fallback_response(self, user_message: str, clinic_context: str = "") -> str:
        """Generate a simple fallback response when LLM is not available"""
        
        response = "I'm here to help you find the perfect beauty clinic in Japan! "
        
        if clinic_context:
            response += f"\n{clinic_context}\n\nWould you like more information about any of these clinics?"
        else:
            response += "\nI can help you:\n"
            response += "- Find beauty clinics by location or service\n"
            response += "- Compare different clinics\n"
            response += "- Provide information about services and prices\n"
            response += "- Guide you through the booking process\n\n"
            response += "Try asking me something like:\n"
            response += "- 'Find me a salon in Shibuya'\n"
            response += "- 'What are the best rated clinics?'\n"
            response += "- 'I'm looking for facial treatments'\n"
        
        return response
    
    def get_booking_help(self, clinic: Dict) -> str:
        """Provide booking assistance for a specific clinic"""
        help_text = f"""
📅 **Booking Help for {clinic['name']}**

To book an appointment:

1. **Call the clinic:**
   Phone: {clinic.get('phone', 'N/A')}
   (English support may be limited - consider using a translation app)

2. **Visit their website:**
   {clinic.get('website', 'N/A')}
   (Many clinics have online booking systems)

3. **What to say when booking:**
   - Your name
   - Desired service: {', '.join(clinic.get('services', [])[:2])}
   - Preferred date and time
   - Special requests (English-speaking staff, etc.)

4. **Useful Japanese phrases:**
   - "Eigo wo hanasemasu ka?" (Do you speak English?)
   - "Yoyaku wo shitai desu" (I'd like to make a reservation)
   - "Eigo taiou wa arimasu ka?" (Is English support available?)

**Tips:**
- Book in advance, especially for popular clinics
- Confirm the price before your appointment
- Bring cash (many clinics don't accept cards)
- Arrive 10 minutes early

Need help with anything else?
"""
        return help_text


if __name__ == "__main__":
    # Test the advisor
    advisor = BeautyAdvisor()
    
    print("Testing Beauty Advisor...")
    response = advisor.chat("What are the best salons in Tokyo?")
    print(f"\nResponse:\n{response}")
