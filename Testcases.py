import unittest
from flask import Flask
from flask_pymongo import PyMongo
from mongo_connection import MongoDBConnection
from api import TestCase  # Update the import statement
import json
from api import app

class TestDepartmentAPI(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        app.config["MONGO_URI"] = "mongodb://localhost:27017/test_db"  # Use a test database
        return app

    def setUp(self):
        # Set up test data or perform any necessary setup
        self.mongo_connection = MongoDBConnection(app.config["MONGO_URI"])
        self.departments_collection = self.mongo_connection.get_departments_collection()
        self.departments_collection.delete_many({})

    def tearDown(self):
        # Clean up after each test
        self.departments_collection.delete_many({})

    def test_get_departments(self):
        # Test GET request to /departments
        response = self.client.get('/departments')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'departments': []})

        # Add a department and test again
        self.departments_collection.insert_one({'name': 'Test Department'})
        response = self.client.get('/departments')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'departments': ['Test Department']})

    def test_add_department(self):
        # Test POST request to /departments
        data = {'name': 'New Department'}
        response = self.client.post('/departments', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Department added successfully'})

        # Check if the department is added to the database
        department = self.departments_collection.find_one({'name': 'New Department'})
        self.assertIsNotNone(department)

    def test_add_invalid_department(self):
        # Test POST request with invalid data to /departments
        data = {'invalid_key': 'Invalid Department'}
        response = self.client.post('/departments', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Invalid department name'})

    def test_delete_department(self):
        # Test DELETE request to /departments/<department_id>
        department_id = str(self.departments_collection.insert_one({'name': 'Test Department'}).inserted_id)
        response = self.client.delete(f'/departments/{department_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Department deleted successfully'})

        # Check if the department is deleted from the database
        department = self.departments_collection.find_one({'_id': department_id})
        self.assertIsNone(department)

    def test_delete_nonexistent_department(self):
        # Test DELETE request with nonexistent department_id to /departments/<department_id>
        response = self.client.delete('/departments/nonexistent_id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Department not found'})

if __name__ == '__main__':
    unittest.main()
