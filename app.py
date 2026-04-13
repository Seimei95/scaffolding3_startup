"""
app.py
Flask application template for the warm-up assignment

Students need to implement the API endpoints as specified in the assignment.
"""

import traceback

from flask import Flask, jsonify, render_template, request

from starter_preprocess import TextPreprocessor

app = Flask(__name__)
preprocessor = TextPreprocessor()


@app.route("/")
def home():
    """Render a simple HTML form for URL input"""
    return render_template("index.html")


@app.route("/health")
def health_check():
    """Simple health check endpoint"""
    return jsonify(
        {"status": "healthy", "message": "Text preprocessing service is running"}
    )


@app.route("/api/clean", methods=["POST"])
def clean_text():
    """
    TODO: Implement this endpoint for Part 3

    API endpoint that accepts a URL and returns cleaned text

    Expected JSON input:
        {"url": "https://www.gutenberg.org/files/1342/1342-0.txt"}

    Returns JSON:
        {
            "success": true/false,
            "cleaned_text": "...",
            "statistics": {...},
            "summary": "...",
            "error": "..." (if applicable)
        }
    """
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify(
            {"success": False, "error": "Missing 'url' field in JSON payload"}
        ), 400

    url = data["url"]

    try:
        raw_text = preprocessor.fetch_from_url(url)
        cleaned_gutenberg = preprocessor.clean_gutenberg_text(raw_text)
        final_cleaned_text = preprocessor.normalize_text(cleaned_gutenberg)

        stats = preprocessor.get_text_statistics(final_cleaned_text)
        summary = preprocessor.create_summary(final_cleaned_text)

        return jsonify(
            {
                "success": True,
                "cleaned_text": final_cleaned_text,
                "statistics": stats,
                "summary": summary,
            }
        ), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

        # TODO: Get JSON data from request
        # TODO: Extract URL from the JSON
        # TODO: Validate URL (should be .txt)
        # TODO: Use preprocessor.fetch_from_url()
        # TODO: Clean the text with preprocessor.clean_gutenberg_text()
        # TODO: Normalize with preprocessor.normalize_text()
        # TODO: Get statistics with preprocessor.get_text_statistics()
        # TODO: Create summary with preprocessor.create_summary()
        # TODO: Return JSON response


@app.route("/api/analyze", methods=["POST"])
def analyze_text():
    """
    TODO: Implement this endpoint for Part 3

    API endpoint that accepts raw text and returns statistics only

    Expected JSON input:
        {"text": "Your raw text here..."}

    Returns JSON:
        {
            "success": true/false,
            "statistics": {...},
            "error": "..." (if applicable)
        }
    """
    # TODO: Get JSON data from request
    # TODO: Extract text from the JSON
    # TODO: Get statistics with preprocessor.get_text_statistics()
    # TODO: Return JSON response
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify(
            {"success": False, "error": "Missing 'text' field in JSON payload"}
        ), 400

    text = data["text"]

    try:
        stats = preprocessor.get_text_statistics(text)
        return jsonify({"success": True, "statistics": stats})
    except Exception as e:
        return jsonify(
            {"success": False, "error": f"Failed to analyze text: {str(e)}"}
        ), 500


# Error handlers
"""@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500"""

if __name__ == "__main__":
    print("🚀 Starting Text Preprocessing Web Service...")
    print("📖 Available endpoints:")
    print("   GET  /           - Web interface")
    print("   GET  /health     - Health check")
    print("   POST /api/clean  - Clean text from URL")
    print("   POST /api/analyze - Analyze raw text")
    print()
    print("🌐 Open your browser to: http://localhost:5001")
    print("⏹️  Press Ctrl+C to stop the server")

    app.run(debug=True, port=5001, host="0.0.0.0")
