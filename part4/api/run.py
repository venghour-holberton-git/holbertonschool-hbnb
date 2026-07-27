#!/usr/bin/python3


from app import create_app
from app.extensions import db
from flask_cors import CORS

app = create_app()
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
