from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

# Load environment variables from .env
load_dotenv()

# Get Mongo credentials
username = os.getenv("MONGO_USER")
raw_password = os.getenv("MONGO_PASS")
cluster = os.getenv("MONGO_CLUSTER", "cluster0.ahac7me.mongodb.net")  # default if not set

# Safety check
if not username or not raw_password:
    raise EnvironmentError("MONGO_USER or MONGO_PASS is not set in environment variables.")

# Safely encode the password
password = quote_plus(raw_password)

# MongoDB URI
uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority"
client = MongoClient(uri)

# Connect to database and collection
db = client.freelance_projects
projects_collection = db.projects

@app.route('/projects', methods=['GET'])
def get_projects():
    projects = []
    for proj in projects_collection.find():
        proj['_id'] = str(proj['_id'])  # Convert ObjectId to string
        projects.append(proj)
    return jsonify(projects)

@app.route('/projects', methods=['POST'])
def add_project():
    data = request.json
    projects_collection.update_one(
        {'title': data['title']},
        {'$set': data},
        upsert=True
    )
    return jsonify({'message': 'Project added/updated'}), 201

@app.route('/projects/<project_id>/status', methods=['PUT'])
def update_status(project_id):
    status = request.json.get('status')
    if not status:
        return jsonify({'error': 'No status provided'}), 400
    projects_collection.update_one({'_id': ObjectId(project_id)}, {'$set': {'status': status}})
    return jsonify({'message': 'Status updated'})

@app.route('/earnings', methods=['GET'])
def calculate_earnings():
    pipeline = [
        {'$match': {'status': 'Completed'}},
        {'$group': {'_id': None, 'total': {'$sum': '$amount'}}}
    ]
    result = list(projects_collection.aggregate(pipeline))
    total = result[0]['total'] if result else 0
    return jsonify({'total_earnings': total})

if __name__ == '__main__':
    app.run(debug=True)
