from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from mongo_connection import MongoDBConnection

app = Flask(__name__)
app.config["MONGO_URI"] = "your_mongodb_connection_uri"
mongo_connection = MongoDBConnection(app.config["MONGO_URI"])
mongo = PyMongo(app)

@app.route('/departments', methods=['GET'])
def get_departments():
    departments_collection = mongo_connection.get_departments_collection()
    departments = departments_collection.find()
    return jsonify({'departments': [department['name'] for department in departments]})

@app.route('/departments', methods=['POST'])
def add_department():
    data = request.get_json()
    department_name = data.get('name')
    if department_name:
        departments_collection = mongo_connection.get_departments_collection()
        departments_collection.insert_one({'name': department_name})
        return jsonify({'message': 'Department added successfully'})
    else:
        return jsonify({'error': 'Invalid department name'}), 400

@app.route('/departments/<department_id>', methods=['DELETE'])
def delete_department(department_id):
    departments_collection = mongo_connection.get_departments_collection()
    result = departments_collection.delete_one({'_id': department_id})
    if result.deleted_count > 0:
        return jsonify({'message': 'Department deleted successfully'})
    else:
        return jsonify({'error': 'Department not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
