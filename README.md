# PROJECT BEAUTY 🌸

**Empowering global travelers to explore Japan's vast aesthetic and beauty scene with ease.**

Through an **AI Beauty Advisor**, users can find, compare, and understand Japan's top clinics — all in English.

## Mission Statement

> "To make Japanese beauty transparent and accessible to the world."

## ✨ Quick Start

Try the system in 3 simple steps:

```bash
# 1. Install (core dependencies only)
pip install beautifulsoup4 requests python-dotenv

# 2. Run the demo
python demo.py

# 3. Start the interactive advisor
python beauty_advisor.py
```

That's it! The system works out of the box with sample data and no API keys required.

## Features

- 🔍 **Web Scraping**: Automatically scrape clinic data from beauty.hotpepper.jp
- 🤖 **AI Beauty Advisor**: Intelligent assistant to help find and compare clinics
- 🌐 **English Translation**: All content automatically translated from Japanese
- 📅 **Booking Assistance**: Guided help to book appointments
- 💬 **Natural Conversation**: Chat with the AI advisor in plain English

## Installation

1. Clone the repository:
```bash
git clone https://github.com/StabroApp/beauty-.git
cd beauty-
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Configuration

Create a `.env` file with the following:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Scrape Beauty Clinic Data

```bash
python scraper/hotpepper_scraper.py --location tokyo --category salon
```

### Run the AI Beauty Advisor

```bash
python beauty_advisor.py
```

Then interact with the advisor:
```
> What are the best beauty clinics in Shibuya?
> I'm looking for a facial treatment, what do you recommend?
> How can I book an appointment at [clinic name]?
```

## Project Structure

```
beauty-/
├── scraper/              # Web scraping modules
│   ├── hotpepper_scraper.py
│   └── data_processor.py
├── advisor/              # AI Beauty Advisor
│   ├── advisor_agent.py
│   ├── translator.py
│   └── vector_store.py
├── data/                 # Scraped data storage
├── beauty_advisor.py     # Main CLI interface
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## How It Works

1. **Scraping**: The scraper fetches clinic information from beauty.hotpepper.jp including:
   - Clinic names and locations
   - Services offered
   - Prices
   - Reviews and ratings
   - Contact information

2. **Translation**: All Japanese text is automatically translated to English using AI-powered translation

3. **AI Advisor**: Uses LangChain and OpenAI to:
   - Understand user queries in natural language
   - Search through the clinic database
   - Provide personalized recommendations
   - Guide users through the booking process

4. **Vector Search**: Clinic data is stored in a vector database for semantic search

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Disclaimer

This project is for educational and informational purposes. Always verify clinic information and booking details directly with the clinics.

## 📚 Documentation

- **[USAGE.md](USAGE.md)** - Comprehensive usage guide with examples
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to the project
- **[examples.py](examples.py)** - 8 example use cases
- **[demo.py](demo.py)** - Full system demonstration

## 🧪 Testing

Run the test suite:

```bash
python tests.py
```

All tests should pass, verifying:
- Scraper functionality
- Data processing
- AI advisor capabilities
- Translation features

## 🎯 Example Usage

### CLI Commands

```bash
# Scrape clinics from different locations
python scraper/hotpepper_scraper.py --location tokyo --category salon
python scraper/hotpepper_scraper.py --location osaka --category nail

# Run examples
python examples.py

# Start interactive advisor
python beauty_advisor.py
```

### In the Interactive Advisor

```
You: Find me the best salons in Shibuya
You: I'm looking for nail services in Osaka
You: Show me clinics with English-speaking staff
You: /top          # Show top-rated clinics
You: /stats         # Show statistics
You: /help          # Show all commands
```

## 🚀 Advanced Features

For full AI capabilities, install optional dependencies:

```bash
pip install langchain langchain-openai openai chromadb deep-translator
```

Then set your OpenAI API key in `.env`:
```
OPENAI_API_KEY=your_key_here
```

## Disclaimer

This project is for educational and informational purposes. Always verify clinic information and booking details directly with the clinics.