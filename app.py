from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load MongoDB credentials from .env
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER", "cluster0.m6xx0vr.mongodb.net")  # default value
DB_NAME = os.getenv("DB_NAME", "freelance_project_tracker")

# MongoDB connection URI
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_CLUSTER}/?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
projects_collection = db["projects"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = list(projects_collection.find({}, {'_id': 0}))
    return jsonify(projects)

@app.route('/api/projects', methods=['POST'])
def add_project():
    data = request.json
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400
    try:
        projects_collection.insert_one(data)
        return jsonify({'message': 'Project added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
