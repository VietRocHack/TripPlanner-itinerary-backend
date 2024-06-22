from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from openai import OpenAI

import boto3
from boto3.dynamodb.conditions import Key, Attr

import uuid, time, json
from dotenv import load_dotenv

import requests

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# OpenAI API support
# client = OpenAI(api_key=settings.openapi_key)
client = OpenAI()
model = "gpt-3.5-turbo"

# AWS DynamoDB support
dynamodb = boto3.resource('dynamodb')
itinerary_table = dynamodb.Table('Itineraries')

# HTTP codes
http_ok = 200
http_created = 201
http_bad_request = 400

'''
Use this call to test connection
'''
@app.route("/")
@cross_origin()
def index():
    return jsonify("Hello world"), http_ok

'''
In theory, should be deprecated soon. Please use generate_itinerary_v2
'''
@app.route("/generate_itinerary", methods=['GET'])
@cross_origin()
def generate_itinerary():
    user_prompt = request.args.get("prompt")
    if user_prompt == "":
        return jsonify("Error: No prompt found"), http_bad_request
    
    system_prompt_file = open("./prompts/one_day_prompt_system_json.txt", "r")
    system_prompt = system_prompt_file.read()

    completion = client.chat.completions.create(
        model = model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return completion.choices[0].message.content, http_created

'''
Returns a single STRING containing the UUID of the itinerary on the database
'''
@app.route("/generate_itinerary_v2", methods=['POST'])
@cross_origin()
def generate_itinerary_v2():
    # Generate an itinerary from OpenAI
    user_prompt = request.args.get("prompt")
    if user_prompt == "":
        return jsonify("Error: No prompt found"), http_bad_request

    system_prompt_file = open("./prompts/one_day_prompt_system_json.txt", "r")
    system_prompt = system_prompt_file.read()

    completion = client.chat.completions.create(
        model = model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    itinerary = str(completion.choices[0].message.content)

    # Put the itinerary in DynamoDB, generating other fields
    itinerary_uuid = str(uuid.uuid4())
    itinerary_timestamp = str(time.time())

    itinerary_table.put_item(
        Item={
            'id': itinerary_uuid,
            'timestamp': itinerary_timestamp,
            'itinerary': itinerary,
            'prompt': user_prompt
        }
    )

    return itinerary_uuid, http_created

@app.route('/get_itinerary', methods=['GET'])
@cross_origin()
def get_itinerary():
    # Process params
    id = request.args.get('uuid')
    if id == "":
        return "Error: You must specify an UUID.", http_bad_request
    fields = request.args.get('fields')
    if fields == "":
        return "Error: You must specify fields.", http_bad_request
    
    # Get a response from DynamoDB
    response = itinerary_table.query(
        KeyConditionExpression=Key('id').eq(id),
        ProjectionExpression=fields
    )

    return response['Items'][0], http_ok




if __name__ == "__main__":
    app.run(port=8000)