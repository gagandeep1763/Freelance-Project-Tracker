from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Credentials
username = quote_plus(os.getenv("MONGO_USER"))
password = quote_plus(os.getenv("MONGO_PASS"))

# Flask app setup
app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

# MongoDB connection
uri = f"mongodb+srv://{username}:{password}@cluster0.ahac7me.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['freelance_projects']
projects_collection = db['projects']

# Serve index.html
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Get all projects
@app.route('/projects', methods=['GET'])
def get_projects():
    try:
        projects = []
        for project in projects_collection.find():
            project['_id'] = str(project['_id'])
            projects.append(project)
        return jsonify(projects), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add or update a project
@app.route('/projects', methods=['POST'])
def add_or_update_project():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Missing project data'}), 400

        query = {'title': data.get('title')}
        update = {'$set': data}
        projects_collection.update_one(query, update, upsert=True)
        return jsonify({'message': 'Project added/updated'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update project status
@app.route('/projects/<project_id>/status', methods=['PUT'])
def update_project_status(project_id):
    try:
        status = request.json.get('status')
        if not status:
            return jsonify({'error': 'Missing status'}), 400

        result = projects_collection.update_one(
            {'_id': ObjectId(project_id)},
            {'$set': {'status': status}}
        )
        if result.matched_count == 0:
            return jsonify({'error': 'Project not found'}), 404

        return jsonify({'message': 'Status updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get total earnings
@app.route('/earnings', methods=['GET'])
def get_earnings():
    try:
        pipeline = [
            {'$match': {'status': 'Completed'}},
            {'$group': {'_id': None, 'total': {'$sum': '$amount'}}}
        ]
        result = list(projects_collection.aggregate(pipeline))
        total = result[0]['total'] if result else 0
        return jsonify({'total_earnings': total}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run server
if __name__ == '__main__':
    app.run(debug=True, threaded=False, use_reloader=False)

