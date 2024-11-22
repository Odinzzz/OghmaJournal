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
        self.mock_tags = []  # Mock storage for tags

    def mock_db_execute(self, query, *params):
        """Mock database execute function."""
        if query.startswith("INSERT INTO tags"):
            tag, tag_type = params[0], params[1]
            # Check for duplicate tags
            for mock_tag in self.mock_tags:
                if mock_tag['tag'] == tag:
                    return [{'id': str(uuid.uuid4()), 'tag': tag, 'tag_type': tag_type}]
            # Add the tag to mock storage
            self.mock_tags.append({'id': str(uuid.uuid4()), 'tag': tag, 'tag_type': tag_type})
            return True

        elif query.startswith("SELECT * FROM tags WHERE tag = ?;"):
            tag = params[0]
            # Return existing tag if found
            return [mock_tag for mock_tag in self.mock_tags if mock_tag['tag'] == tag]

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
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], 'Fail to create Tag: tag and tag_Type cannot be Null')

    def test_add_tag_invalid_format(self):
        """Test adding a tag with an invalid format."""
        data = {
            "tag": "InvalidTagFormat",
            "tag_type": "character"
        }
        response = self.app.post("/db/add_tag", json=data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Fail to create Tag: Invalid tag format")

    def test_add_tag_missing_tag(self):
        """Test adding a tag with a missing tag."""
        data = {
            "tag_type": "character"
        }  # Missing 'tag'
        response = self.app.post("/db/add_tag", json=data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Fail to create Tag: tag and tag_Type cannot be Null")
    
    def test_add_tag_existing_tag(self):
        """Test adding a tag that already exists."""
        # Add a tag to the mock database
        existing_tag = {
            "id": str(uuid.uuid4()),
            "tag": "@JournalEntry[already]{exist}",
            "tag_type": "exist"
        }
        self.mock_tags.append(existing_tag)

        # Attempt to add the same tag again
        data = {
            "tag": existing_tag["tag"],
            "tag_type": existing_tag["tag_type"]
        }
        response = self.app.post("/db/add_tag", json=data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], f"Fail to create Tag: {data['tag']} already exists")


if __name__ == "__main__":
    unittest.main()

