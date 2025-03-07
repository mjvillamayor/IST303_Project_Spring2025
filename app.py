from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Flask App is running without package import issues!"})

if __name__ == '__main__':
    app.run(debug=True)
