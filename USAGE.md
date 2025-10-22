# Usage Guide - PROJECT BEAUTY

This guide provides detailed instructions on how to use the PROJECT BEAUTY AI Beauty Advisor.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Using the Scraper](#using-the-scraper)
4. [Using the AI Advisor](#using-the-ai-advisor)
5. [Command Reference](#command-reference)
6. [Examples](#examples)
7. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/StabroApp/beauty-.git
cd beauty-

# Install core dependencies
pip install -r requirements.txt
```

### Optional: Full AI Features

To enable full AI features with OpenAI integration:

1. Get an OpenAI API key from https://platform.openai.com/
2. Install additional dependencies:
   ```bash
   pip install langchain langchain-openai langchain-community openai chromadb
   ```
3. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` and add your API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Optional: Translation Features

To enable automatic Japanese-to-English translation:

```bash
pip install deep-translator
```

## Quick Start

### Run the Demo

The easiest way to get started is to run the demo:

```bash
python demo.py
```

This will showcase all the main features of the system.

### Run the Interactive Advisor

Start the interactive AI Beauty Advisor:

```bash
python beauty_advisor.py
```

## Using the Scraper

### Basic Scraping

Scrape beauty clinic data from different locations and categories:

```bash
# Scrape Tokyo salons
python scraper/hotpepper_scraper.py --location tokyo --category salon

# Scrape Osaka nail salons
python scraper/hotpepper_scraper.py --location osaka --category nail

# Scrape Kyoto esthetic clinics
python scraper/hotpepper_scraper.py --location kyoto --category esthetic
```

### Available Locations

- tokyo
- osaka
- kyoto

### Available Categories

- salon (hair salons)
- nail (nail salons)
- eyelash (eyelash services)
- esthetic (facial and body treatments)

### Custom Output

Save to a custom filename:

```bash
python scraper/hotpepper_scraper.py --location tokyo --category salon --output my_data.json
```

## Using the AI Advisor

### Starting the Advisor

```bash
python beauty_advisor.py
```

### Interactive Commands

Once running, you can use these commands:

- `/help` - Show help information
- `/search` - Interactive search for clinics
- `/top` - Show top-rated clinics
- `/stats` - Show statistics about loaded clinics
- `/scrape` - Scrape new clinic data
- `/quit` - Exit the program

### Natural Language Queries

You can also just chat naturally with the advisor:

```
You: What are the best beauty salons in Shibuya?
You: I'm looking for a facial treatment in Tokyo
You: Show me nail salons with high ratings
You: How can I book an appointment?
```

## Command Reference

### `/search` - Interactive Search

Prompts you for location and category, then searches for matching clinics.

**Example:**
```
You: /search
📍 Location (e.g., tokyo, osaka): tokyo
💅 Category (salon, nail, eyelash, esthetic): salon
```

### `/top` - Top Rated Clinics

Shows the top 5 highest-rated clinics in the database.

**Example:**
```
You: /top

⭐ Top 5 Rated Clinics:
1. Roppongi Beauty Salon 5 - 4.8/5
   📍 Roppongi, tokyo
   💰 ¥7000 - ¥16000

2. Harajuku Beauty Salon 4 - 4.6/5
   📍 Harajuku, tokyo
   💰 ¥6000 - ¥14000
...
```

### `/stats` - Statistics

Displays statistics about the clinic database.

**Example:**
```
You: /stats

📊 Clinic Statistics:
Total Clinics: 5
Average Rating: 4.40/5

Categories:
  - Salon: 5

Locations:
  - Tokyo: 5
```

### `/scrape` - Scrape New Data

Interactively scrape new clinic data and add it to the database.

**Example:**
```
You: /scrape
📍 Location (e.g., tokyo, osaka, kyoto): osaka
💅 Category (salon, nail, eyelash, esthetic): nail

🔍 Scraping new clinic data...
✅ Scraped 5 clinics!
```

## Examples

### Example 1: Finding a Salon in a Specific Area

```
You: Find me a hair salon in Shibuya

🤖 AI Advisor:
I'm here to help you find the perfect beauty clinic in Japan!

Relevant clinics:

📍 **Shibuya Beauty Salon 1**
   Category: Salon
   Location: Shibuya, Tokyo
   Rating: ⭐⭐⭐⭐ 4.0/5 (50 reviews)
   
   Services: Hair Cut, Hair Color, Perm
   Price Range: ¥3000 - ¥8000
   ...
```

### Example 2: Comparing Multiple Clinics

```
You: Show me the best rated salons in Tokyo

🤖 AI Advisor:
Here are the top-rated salons in Tokyo:

📍 **Roppongi Beauty Salon 5**
   Rating: ⭐⭐⭐⭐⭐ 4.8/5 (150 reviews)
   ...

📍 **Harajuku Beauty Salon 4**
   Rating: ⭐⭐⭐⭐ 4.6/5 (125 reviews)
   ...
```

### Example 3: Getting Booking Help

```
You: How do I book an appointment at Shibuya Beauty Salon 1?

🤖 AI Advisor:
📅 **Booking Help for Shibuya Beauty Salon 1**

To book an appointment:

1. **Call the clinic:**
   Phone: 03-1000-2000
   
2. **Visit their website:**
   https://beauty.hotpepper.jp/slnH000100000/
   
3. **Useful Japanese phrases:**
   - "Eigo wo hanasemasu ka?" (Do you speak English?)
   - "Yoyaku wo shitai desu" (I'd like to make a reservation)
   ...
```

## Troubleshooting

### "No clinic data found"

**Problem:** The advisor can't find any clinic data.

**Solution:** Run the scraper first:
```bash
python scraper/hotpepper_scraper.py --location tokyo --category salon
```

### "OPENAI_API_KEY not found"

**Problem:** The system can't find your OpenAI API key.

**Solution:** This is just a warning. The system will work in fallback mode without AI features. To enable full AI features:
1. Get an API key from https://platform.openai.com/
2. Create a `.env` file with `OPENAI_API_KEY=your_key_here`

### "ModuleNotFoundError"

**Problem:** Required Python packages are not installed.

**Solution:** Install the dependencies:
```bash
pip install -r requirements.txt
```

For optional features:
```bash
# For AI features
pip install langchain langchain-openai openai chromadb

# For translation
pip install deep-translator
```

### Search Returns No Results

**Problem:** Searching for clinics returns no results.

**Solution:** 
1. Make sure you've scraped data for that location/category
2. Try broader search terms
3. Use `/stats` to see what data is available

### Cannot Connect to OpenAI

**Problem:** Error connecting to OpenAI API.

**Solution:**
1. Check your API key is correct
2. Ensure you have internet connectivity
3. Verify your OpenAI account has credits
4. The system will automatically fall back to basic mode if OpenAI is unavailable

## Tips and Best Practices

1. **Start with the Demo**: Run `python demo.py` first to understand all features
2. **Scrape Multiple Locations**: Build a comprehensive database by scraping multiple locations and categories
3. **Use Natural Language**: The AI understands natural questions better than keyword searches
4. **Check Stats Regularly**: Use `/stats` to understand what data you have
5. **Update Data**: Re-run the scraper periodically to get fresh data

## Getting Help

If you encounter issues not covered here:

1. Check the main README.md
2. Run `python beauty_advisor.py` and type `/help`
3. Open an issue on GitHub

## Next Steps

- Explore different locations and categories
- Try various natural language queries
- Experiment with the booking assistance features
- Contribute to the project on GitHub

Happy beauty clinic hunting! 🌸
