# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        # Add your actual analysis logic here
        return jsonify({
            'status': 'success',
            'risk_score': 75,  # Replace with real calculation
            'face_verified': False,
            'details': {
                'face_match': 0.65,
                'metadata': {'followers': 150, 'following': 1800}
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)