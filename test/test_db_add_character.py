import unittest
from flask import Flask, jsonify
import json

# Import your Flask app and the database module
from app import app, db

class TestAddCharacter(unittest.TestCase):

    def setUp(self):
        """Set up the test client and mock the database."""
        self.app = app.test_client()
        self.app.testing = True
        self.db_mock = db
        self.db_mock.execute = self.mock_db_execute
    
    def mock_db_execute(self, query, *params):
        """
        Mock database execute function. 
        Add logic here to simulate database behavior for different test cases.
        """
        if query.startswith("SELECT * FROM tags WHERE tag = ?;"):
            if params[0] == "@JournalEntry[existing]{tag}":  # Simulate a duplicate tag
                return [1]
            return []

        if query.startswith("SELECT * FROM characters WHERE name = ?;"):
            if params[0] == "ExistingCharacter":  # Simulate a duplicate character
                return [1]
            return []

        return []  # Default: no results

    def test_add_character_success(self):
        """Test adding a valid character."""
        data = {
            "name": "ValidName",
            "classe": "Warrior",
            "type": "NPC",
            "tag": "@JournalEntry[ValidFoundry]{ValidAlias}"
        }
        response = self.app.post("/db/add_character", json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("id", response_data)
        self.assertEqual(response_data["name"], "ValidName")
        self.assertEqual(response_data["tag"], data["tag"])

    def test_add_character_missing_fields(self):
        """Test adding a character with missing required fields."""
        data = {"classe": "Warrior", "type": "NPC"}  # Missing 'name' and 'tag'
        response = self.app.post("/db/add_character", json=data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Fail to create character: Name and Tag cannot be Null")

    def test_add_character_invalid_tag_format(self):
        """Test adding a character with an invalid tag format."""
        data = {
            "name": "InvalidTagCharacter",
            "classe": "Mage",
            "type": "Player",
            "tag": "InvalidTagFormat"
        }
        response = self.app.post("/db/add_character", json=data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Fail to create character: Tag must be formated like @JournalEntry[foundry_name]{alias}")

    def test_add_character_duplicate_tag(self):
        """Test adding a character with a duplicate tag."""
        data = {
            "name": "NewCharacter",
            "classe": "Thief",
            "type": "NPC",
            "tag": "@JournalEntry[existing]{tag}"
        }
        response = self.app.post("/db/add_character", json=data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Fail to create character: Tag already exist")

    def test_add_character_duplicate_name(self):
        """Test adding a character with a duplicate name."""
        data = {
            "name": "ExistingCharacter",
            "classe": "Cleric",
            "type": "Player",
            "tag": "@JournalEntry[NewFoundry]{Alias}"
        }
        response = self.app.post("/db/add_character", json=data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Fail to create character: Character already exist")

if __name__ == "__main__":
    unittest.main()
