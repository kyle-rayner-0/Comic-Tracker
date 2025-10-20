from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8000 * 1024 * 1024  # 500 MB limit

INDEX_FILE = 'index.html'

# Serve the index page
@app.route('/')
def home():
    return send_file(INDEX_FILE)

# Save updated HTML
@app.route('/save', methods=['POST'])
def save():
    content = request.form.get('html')
    if content:
        try:
            with open(INDEX_FILE, 'w', encoding='utf-8') as f:
                f.write(content)
            return jsonify({"status": "success", "message": "Saved successfully!"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "error", "message": "No content received!"}), 400

# Handle file too large
@app.errorhandler(413)
def too_large(e):
    return jsonify({"status": "error", "message": "File too large (limit 500 MB)!"}), 413

if __name__ == '__main__':
    app.run(debug=True)
