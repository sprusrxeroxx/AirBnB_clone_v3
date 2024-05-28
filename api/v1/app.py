#!/usr/bin/python3
"""
Creates a Flask app and registers the blueprint app_views to instance of app
"""
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_engine(exception):
    """Close the current SQLAlchemy Session"""
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """Return a JSON-formatted 404 status code response"""
    return jsonify({"error": "Not found"}), 404

def main():
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = getenv('HBNB_API_PORT', 5000)
    app.run(debug=True, host=HOST, port=PORT, threaded=True)

if __name__ == "__main__":
    main()

