from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    places = requests.get("http://127.0.0.1:5000/api/v1/places/").json()
    print(f"here they are {places}")
    return render_template('index.html', places=places)

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)