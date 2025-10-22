#!/usr/bin/env python3
"""
PROJECT BEAUTY - Flask Web Application for Cloud Run

Main web application entrypoint for Cloud Run deployment.
Provides REST API for the AI Beauty Advisor.
"""

import os
import sys
import json
import logging
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    logger.info("Note: python-dotenv not installed. Using environment variables directly.")

from advisor.advisor_agent import BeautyAdvisor
from scraper.data_processor import DataProcessor

# Initialize Flask app
app = Flask(__name__)

# Initialize the Beauty Advisor
advisor = None


def get_advisor():
    """Get or initialize the Beauty Advisor instance"""
    global advisor
    if advisor is None:
        api_key = os.getenv("OPENAI_API_KEY")
        advisor = BeautyAdvisor(api_key=api_key)
    return advisor


@app.route("/", methods=["GET"])
def home():
    """Home endpoint with API information"""
    return jsonify({
        "name": "PROJECT BEAUTY - AI Beauty Advisor API",
        "version": "1.0.0",
        "description": "AI Beauty Advisor for Japanese Clinics",
        "endpoints": {
            "/": "API information (this page)",
            "/health": "Health check endpoint",
            "/api/chat": "Chat with AI advisor (POST)",
            "/api/clinics": "Get all clinics (GET)",
            "/api/clinics/search": "Search clinics (GET with ?q=query)",
            "/api/clinics/top": "Get top-rated clinics (GET)",
            "/api/stats": "Get clinic statistics (GET)"
        }
    })


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for Cloud Run"""
    try:
        advisor_instance = get_advisor()
        clinic_count = len(advisor_instance.clinics) if advisor_instance.clinics else 0
        
        return jsonify({
            "status": "healthy",
            "service": "beauty-advisor",
            "clinics_loaded": clinic_count
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        return jsonify({
            "status": "unhealthy",
            "error": "Service is not available"
        }), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    """Chat with the AI Beauty Advisor"""
    try:
        data = request.get_json()
        
        if not data or "message" not in data:
            return jsonify({
                "error": "Missing 'message' field in request body"
            }), 400
        
        message = data["message"]
        advisor_instance = get_advisor()
        
        response = advisor_instance.chat(message)
        
        return jsonify({
            "message": message,
            "response": response
        }), 200
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to process chat request"
        }), 500


@app.route("/api/clinics", methods=["GET"])
def get_clinics():
    """Get all clinics"""
    try:
        advisor_instance = get_advisor()
        clinics = advisor_instance.clinics or []
        
        # Limit to first 50 clinics to avoid large responses
        return jsonify({
            "total": len(clinics),
            "clinics": clinics[:50]
        }), 200
        
    except Exception as e:
        logger.error(f"Get clinics endpoint error: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to retrieve clinics"
        }), 500


@app.route("/api/clinics/search", methods=["GET"])
def search_clinics():
    """Search for clinics by query"""
    try:
        query = request.args.get("q", "")
        
        if not query:
            return jsonify({
                "error": "Missing 'q' query parameter"
            }), 400
        
        advisor_instance = get_advisor()
        results = advisor_instance.search_clinics(query)
        
        return jsonify({
            "query": query,
            "total": len(results),
            "clinics": results[:20]  # Limit to 20 results
        }), 200
        
    except Exception as e:
        logger.error(f"Search clinics endpoint error: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to search clinics"
        }), 500


@app.route("/api/clinics/top", methods=["GET"])
def get_top_clinics():
    """Get top-rated clinics"""
    try:
        limit = int(request.args.get("limit", "10"))
        limit = min(limit, 50)  # Cap at 50
        
        advisor_instance = get_advisor()
        processor = advisor_instance.processor
        top_clinics = processor.get_top_rated(limit)
        
        return jsonify({
            "total": len(top_clinics),
            "clinics": top_clinics
        }), 200
        
    except Exception as e:
        logger.error(f"Get top clinics endpoint error: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to retrieve top-rated clinics"
        }), 500


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get clinic statistics"""
    try:
        advisor_instance = get_advisor()
        processor = advisor_instance.processor
        stats = processor.get_statistics()
        
        return jsonify(stats), 200
        
    except Exception as e:
        logger.error(f"Get stats endpoint error: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to retrieve statistics"
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "message": "Please check the API documentation at /"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "message": str(error)
    }), 500


if __name__ == "__main__":
    # Get port from environment variable (Cloud Run sets this)
    port = int(os.getenv("PORT", 8080))
    
    # Initialize advisor on startup
    print("Initializing AI Beauty Advisor...")
    get_advisor()
    print(f"Loaded {len(advisor.clinics) if advisor.clinics else 0} clinics")
    
    # Run the Flask app
    print(f"Starting Flask app on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
