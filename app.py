from flask import Flask, request, jsonify, redirect
from datetime import datetime, timedelta
from urllib.parse import urlparse
import random
import sqlite3
import string

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('url_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls (
                    short_url TEXT PRIMARY KEY,
                    original_url TEXT NOT NULL,
                    expiration_date TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

# Generate a random short URL
def generate_short_url():
    chars = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(chars) for i in range(6)) 
    return short_url

# Check if the original_url is valid
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

@app.route('/api/shorten', methods=['POST'])
def create_short_url():
    data = request.get_json()

    # Input check
    if not data or 'original_url' not in data:
        return jsonify({
            'success': False,
            'reason': 'Invalid input: "original_url" is required.'
        }), 400 #Bad Request
    
    original_url = data['original_url']

    # Original URL check
    if not is_valid_url(original_url):
        return jsonify({
            'success': False,
            'reason': 'Invalid URL format.'
        }), 400
    
    # URL length check
    if len(original_url) > 2048:
        return jsonify({
            'success': False,
            'reason': 'URL too long.'
        }), 400
    
    short_url = generate_short_url()
    expiration_date = datetime.now() + timedelta(days=30)

    # Save to the database
    conn = sqlite3.connect('url_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO urls (short_url, original_url, expiration_date) VALUES (?, ?, ?)',
              (short_url, original_url, expiration_date.isoformat()))
    conn.commit()
    conn.close()

    return jsonify({
        'short_url': f'http://localhost:5000/{short_url}',
        'expiration_date': expiration_date.isoformat(),
        'success': True,
        'reason': ''
    }), 201 # Created

@app.route('/<short_url>', methods=['GET'])
def redirect_to_original(short_url):
    conn = sqlite3.connect('url_data.db')
    c = conn.cursor()
    c.execute('SELECT original_url, expiration_date FROM urls WHERE short_url = ?', (short_url,))
    result = c.fetchone()
    conn.close()

    if not result:
        return jsonify({'error': 'Short URL not found.'}), 404 #Not Found
    
    original_url, expiration_date = result
    if datetime.fromisoformat(expiration_date) < datetime.now():
        return jsonify({'error': 'Short URL has expired.'}), 410 #Gone
    
    return redirect(original_url)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

