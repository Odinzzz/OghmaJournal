import unittest
from flask import Flask, jsonify, request
import json
import re
import uuid

# Import your Flask app and the database module
from app import app, db

class TestAddTag(unittest.TestCase):

    def setUp(self):
        """Set up the test client and mock the database."""
        self.app = app.test_client()
        self.app.testing = True
        self.db_mock = db
        self.db_mock.execute = self.mock_db_execute
    
    def mock_db_execute(self, query, *params):
        """Mock database execute function."""
        if query.startswith("INSERT INTO tags"):
            return True
        return []

    def test_add_tag_success(self):
        """Test adding a valid tag."""
        data = {
            "tag": "@JournalEntry[Foundry]{Alias}",
            "tag_type": "character"
        }
        response = self.app.post("/db/add_tag", json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("id", response_data)
        self.assertEqual(response_data["tag"], data["tag"])
        self.assertEqual(response_data["tag_type"], data["tag_type"])

    def test_add_tag_missing_fields(self):
        """Test adding a tag with missing required fields."""
        data = {"tag": "@JournalEntry[Foundry]{Alias}"}  # Missing 'tag_type'
        response = self.app.post("/db/add_tag", json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Fail to create Tag: {tag_type} and {tag} cannot be Null")

    def test_add_tag_invalid_format(self):
        """Test adding a tag with an invalid format."""
        data = {
            "tag": "InvalidTagFormat",
            "tag_type": "character"
        }
        response = self.app.post("/db/add_tag", json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Fail to create Tag: {tag} must be formated like @JournalEntry[foundry_name]{alias}")

    def test_add_tag_missing_tag(self):
        """Test adding a tag with a missing tag."""
        data = {
            "tag_type": "character"
        }  # Missing 'tag'
        response = self.app.post("/db/add_tag", json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Fail to create Tag: {tag_type} and {tag} cannot be Null")

if __name__ == "__main__":
    unittest.main()
