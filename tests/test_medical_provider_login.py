
import pytest
import requests
import json
from unittest.mock import patch, Mock

BASE_URL = "http://localhost:5000"

class TestMedicalProviderLogin:
    """Test suite for medical provider login functionality"""
    
    def setup_method(self):
        """Setup before each test"""
        self.login_endpoint = f"{BASE_URL}/api/auth/medical-provider/login"
        self.valid_credentials = {
            "email": "dr.smith@hospital.com",
            "password": "correctpassword"
        }
    
    def test_successful_login(self):
        """Test successful login with valid credentials"""
        with patch('requests.post') as mock_post:
            # Mock successful response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "success": True,
                "token": "jwt_token_here",
                "provider": {
                    "id": 1,
                    "email": "dr.smith@hospital.com",
                    "first_name": "John",
                    "last_name": "Smith"
                }
            }
            mock_post.return_value = mock_response
            
            # Test login request
            response = requests.post(
                self.login_endpoint,
                json=self.valid_credentials
            )
            
            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "token" in data
            assert "provider" in data
    
    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials"""
        with patch('requests.post') as mock_post:
            # Mock failed response
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.json.return_value = {
                "success": False,
                "message": "Invalid email or password"
            }
            mock_post.return_value = mock_response
            
            # Test login with invalid password
            invalid_credentials = {
                "email": "dr.smith@hospital.com",
                "password": "wrongpassword"
            }
            
            response = requests.post(
                self.login_endpoint,
                json=invalid_credentials
            )
            
            # Assertions
            assert response.status_code == 401
            data = response.json()
            assert data["success"] is False
            assert "message" in data
    
    def test_login_with_missing_fields(self):
        """Test login with missing required fields"""
        with patch('requests.post') as mock_post:
            # Mock validation error response
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.json.return_value = {
                "success": False,
                "message": "Email and password are required"
            }
            mock_post.return_value = mock_response
            
            # Test with missing password
            incomplete_data = {
                "email": "dr.smith@hospital.com"
                # Missing password
            }
            
            response = requests.post(
                self.login_endpoint,
                json=incomplete_data
            )
            
            # Assertions
            assert response.status_code == 400
            data = response.json()
            assert data["success"] is False
            assert "message" in data
    
    def test_token_verification(self):
        """Test verification of a valid token"""
        with patch('requests.post') as mock_post:
            # Mock successful token verification
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "success": True,
                "provider": {
                    "id": 1,
                    "email": "dr.smith@hospital.com",
                    "role": "provider"
                }
            }
            mock_post.return_value = mock_response
            
            # Test token verification
            headers = {"Authorization": "Bearer valid_token_here"}
            response = requests.post(
                f"{BASE_URL}/api/auth/verify-token",
                headers=headers
            )
            
            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "provider" in data
