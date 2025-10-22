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

# Google Cloud Storage (Optional)
GCS_BUCKET_NAME=your_gcs_bucket_name_here
GCP_PROJECT_ID=your_gcp_project_id_here
GCS_LOCATION=us-east1
```

### Google Cloud Storage Setup (Optional)

The project supports Google Cloud Storage for data persistence, which is useful for:
- Centralized data storage accessible from multiple machines
- Automatic backups of scraped data
- Efficient use of Google Cloud's free tier (5GB regional storage)

#### Quick Setup:

1. **Create a GCP Project** (if you don't have one):
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable Cloud Storage API**:
   ```bash
   gcloud services enable storage-api.googleapis.com
   ```

3. **Create a Service Account** (for authentication):
   ```bash
   gcloud iam service-accounts create beauty-scraper \
       --display-name="Beauty Scraper Service Account"
   ```

4. **Create and download credentials**:
   ```bash
   gcloud iam service-accounts keys create ~/beauty-scraper-key.json \
       --iam-account=beauty-scraper@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

5. **Set environment variables**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=~/beauty-scraper-key.json
   export GCS_BUCKET_NAME=beauty-clinic-data
   export GCP_PROJECT_ID=your-project-id
   ```

6. **The bucket will be created automatically** when you first run the scraper with `--use-gcs` flag.

#### Free Tier Optimization:

Google Cloud Storage offers:
- **5GB of regional storage** per month (free)
- **5,000 Class A operations** (uploads, list, create bucket)
- **50,000 Class B operations** (downloads, get)

To stay within free tier:
- Use regional storage (us-east1, us-west1, or us-central1)
- Store JSON data (highly compressible)
- Implement automatic cleanup of old data (built-in feature)

## Usage

### Scrape Beauty Clinic Data

```bash
# Basic scraping (saves locally)
python scraper/hotpepper_scraper.py --location tokyo --category salon

# With Google Cloud Storage integration
python scraper/hotpepper_scraper.py --location tokyo --category salon --use-gcs
```

### Google Cloud Storage Operations

```python
from scraper.gcs_storage import GCSStorage

# Initialize storage
storage = GCSStorage()

# Upload data
storage.upload_json(clinic_data, "tokyo_salons.json", folder="clinics")

# Download data
data = storage.download_json("clinics/tokyo_salons.json")

# List files
files = storage.list_files(prefix="clinics", suffix=".json")

# Delete old data (older than 30 days)
deleted_count = storage.delete_old_files(prefix="clinics", days_old=30)

# Get bucket information
info = storage.get_bucket_info()
print(f"Total storage used: {info['total_size_mb']} MB")
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
│   ├── data_processor.py
│   └── gcs_storage.py    # Google Cloud Storage integration
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