from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Flask API is running!"})

@app.route('/api/interactions', methods=['POST'])
def get_interactions():
    data = request.get_json()
    drug_names = data.get("drug_names", [])
    interactions = {drug: ["No known interactions"] for drug in drug_names}
    return jsonify({"interactions": interactions})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
