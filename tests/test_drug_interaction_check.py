import pytest
import requests
import json
from unittest.mock import patch, Mock

BASE_URL = "http://localhost:5000"

class TestDrugInteractionCheck:
    """Test suite for automatic drug interaction checking functionality"""
    
    def setup_method(self):
        """Setup before each test"""
        self.interaction_endpoint = f"{BASE_URL}/api/medications/interactions"
        self.auth_headers = {"Authorization": "Bearer test_token"}
        
        # Sample medications for testing
        self.medication1 = {
            "id": 1,
            "name": "Aspirin",
            "active_ingredients": ["acetylsalicylic acid"]
        }
        
        self.medication2 = {
            "id": 2,
            "name": "Warfarin",
            "active_ingredients": ["warfarin sodium"]
        }
        
        self.medication3 = {
            "id": 3,
            "name": "Ibuprofen",
            "active_ingredients": ["ibuprofen"]
        }
    
    def test_detect_known_interaction(self):
        """Test detection of a known interaction between medications"""
        with patch('requests.post') as mock_post:
            # Mock interaction found response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "hasInteractions": True,
                "interactions": [
                    {
                        "medications": ["Aspirin", "Warfarin"],
                        "severity": "high",
                        "description": "Increased risk of bleeding"
                    }
                ]
            }
            mock_post.return_value = mock_response
            
            # Test checking interaction between aspirin and warfarin
            payload = {
                "medications": [
                    self.medication1["id"], 
                    self.medication2["id"]
                ]
            }
            
            response = requests.post(
                self.interaction_endpoint,
                headers=self.auth_headers,
                json=payload
            )
            
            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert data["hasInteractions"] is True
            assert len(data["interactions"]) > 0
            assert data["interactions"][0]["severity"] == "high"
    
    def test_no_interaction_detected(self):
        """Test when no interactions are found between medications"""
        with patch('requests.post') as mock_post:
            # Mock no interaction response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "hasInteractions": False,
                "interactions": []
            }
            mock_post.return_value = mock_response
            
            # Test checking interaction between medications with no known interactions
            payload = {
                "medications": [
                    self.medication1["id"], 
                    self.medication3["id"]
                ]
            }
            
            response = requests.post(
                self.interaction_endpoint,
                headers=self.auth_headers,
                json=payload
            )
            
            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert data["hasInteractions"] is False
            assert len(data["interactions"]) == 0
    
    def test_invalid_medication_ids(self):
        """Test with invalid medication IDs"""
        with patch('requests.post') as mock_post:
            # Mock error response
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.json.return_value = {
                "success": False,
                "message": "Invalid medication ID: 999"
            }
            mock_post.return_value = mock_response
            
            # Test with an invalid medication ID
            payload = {
                "medications": [1, 999]
            }
            
            response = requests.post(
                self.interaction_endpoint,
                headers=self.auth_headers,
                json=payload
            )
            
            # Assertions
            assert response.status_code == 400
            data = response.json()
            assert data["success"] is False
            assert "Invalid medication ID" in data["message"]
    
    def test_check_interaction_unauthorized(self):
        """Test interaction check without authentication"""
        with patch('requests.post') as mock_post:
            # Mock unauthorized response
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.json.return_value = {
                "success": False,
                "message": "Authentication required"
            }
            mock_post.return_value = mock_response
            
            # Test without auth header
            payload = {
                "medications": [
                    self.medication1["id"], 
                    self.medication2["id"]
                ]
            }
            
            response = requests.post(
                self.interaction_endpoint,
                json=payload
                # No auth headers
            )
            
            # Assertions
            assert response.status_code == 401
            data = response.json()
            assert data["success"] is False
    
    def test_interaction_check_with_prescription(self):
        """Test checking interactions when adding a prescription"""
        with patch('requests.post') as mock_post:
            # Mock response for prescription with interaction warning
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {
                "success": True,
                "prescription": {
                    "id": 1,
                    "patient_id": 101,
                    "provider_id": 201,
                    "medication_id": 2,
                    "dosage": "5mg",
                    "frequency": "daily"
                },
                "warnings": {
                    "hasInteractions": True,
                    "interactions": [
                        {
                            "medications": ["Aspirin", "Warfarin"],
                            "severity": "high",
                            "description": "Increased risk of bleeding"
                        }
                    ]
                }
            }
            mock_post.return_value = mock_response
            
            # Test adding a prescription that triggers an interaction warning
            prescription_data = {
                "patient_id": 101,
                "medication_id": 2,  # Warfarin
                "dosage": "5mg",
                "frequency": "daily",
                "start_date": "2023-05-01"
            }
            
            response = requests.post(
                f"{BASE_URL}/api/prescriptions",
                headers=self.auth_headers,
                json=prescription_data
            )
            
            # Assertions
            assert response.status_code == 201
            data = response.json()
            assert data["success"] is True
            assert "warnings" in data
            assert data["warnings"]["hasInteractions"] is True
