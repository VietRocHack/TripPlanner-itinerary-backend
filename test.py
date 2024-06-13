from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify("Hello world")

@app.route("/generate_itinerary")
def generate_itinerary():
    # TODO: recieve a prompt from frontend and generate a JSON itinerary for that prompt
    return ""

def save_to_database():
    # TODO: save the generated prompt in a database
    return ""

if __name__ == "__main__":
    app.run(port=8000)