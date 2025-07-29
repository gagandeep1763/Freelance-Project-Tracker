from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Escape username & password
username = quote_plus(os.getenv("MONGO_USER"))
password = quote_plus(os.getenv("MONGO_PASS"))

# Flask App Setup
app = Flask(__name__)
CORS(app)

# MongoDB Connection
uri = f"mongodb+srv://{username}:{password}@cluster0.ahac7me.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client.freelance_projects
projects_collection = db.projects

# Serve Frontend
@app.route('/')
def home():
    return render_template('index.html')

# Get all projects
@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = []
    for proj in projects_collection.find():
        proj['_id'] = str(proj['_id'])  # Make ObjectId JSON serializable
        projects.append(proj)
    return jsonify(projects)

# Add or update a project
@app.route('/api/projects', methods=['POST'])
def add_project():
    data = request.json
    if not data:
        return jsonify({'error': 'No project data provided'}), 400
    projects_collection.update_one(
        {'name': data['name']},
        {'$set': data},
        upsert=True
    )
    return jsonify({'message': 'Project added/updated'}), 201

# Update project status
@app.route('/api/projects/<project_id>/status', methods=['PUT'])
def update_status(project_id):
    status = request.json.get('status')
    if not status:
        return jsonify({'error': 'No status provided'}), 400
    projects_collection.update_one({'_id': ObjectId(project_id)}, {'$set': {'status': status}})
    return jsonify({'message': 'Status updated'})

# Earnings calculation
@app.route('/api/earnings', methods=['GET'])
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
