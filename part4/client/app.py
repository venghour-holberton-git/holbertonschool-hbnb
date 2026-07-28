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

# @app.route('/place')
# def place():
#     return render_template('place.html')

@app.route('/places/<place_id>')
def place_id(place_id):
    token = request.cookies.get("token")
    response = requests.get(f'http://127.0.0.1:5000/api/v1/places/{place_id}', 
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    data = response.json()
    return render_template('place.html', place_id=place_id, place_data=data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)