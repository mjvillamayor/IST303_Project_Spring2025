import pytest
import requests
import json
import pyotp  # For generating TOTP tokens
from unittest.mock import patch, Mock

BASE_URL = "http://localhost:5000"

class TestAdmin2FA:
    """Test suite for administrator two-factor authentication"""
    
    def setup_method(self):
        """Setup before each test"""
        self.admin_login_endpoint = f"{BASE_URL}/api/auth/admin/login"
        self.verify_2fa_endpoint = f"{BASE_URL}/api/auth/admin/verify-2fa"
        self.setup_2fa_endpoint = f"{BASE_URL}/api/auth/admin/setup-2fa"
        
        self.admin_credentials = {
            "email": "admin@hospital.com",
            "password": "adminPassword123"
        }
        
        # Mock TOTP secret for testing
        self.sample_totp_secret = "JBSWY3DPEHPK3PXP"
    
    def test_admin_login_requires_2fa(self):
        """Test that admin login requires 2FA verification"""
        with patch('requests.post') as mock_post:
            # Mock successful initial login that requires 2FA
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "success": True,
                "message": "2FA verification required",
                "requires2FA": True,
                "tempToken": "temp_session_token_for_2fa"
            }
            mock_post.return_value = mock_response
            
            # Test admin login request
            response = requests.post(
                self.admin_login_endpoint,
                json=self.admin_credentials
            )
            
            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["requires2FA"] is True
            assert "tempToken" in data
    
    def test_verify_valid_2fa_code(self):
        """Test verification of a valid 2FA code"""
        # Generate a valid TOTP code based on the secret
        valid_code = pyotp.TOTP(self.sample_totp_secret).now()
        
        with patch('requests.post') as mock_post:
            # Mock successful 2FA verification response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "success": True,
                "token": "full_access_jwt_token",
                "admin": {
                    "id": 1,
                    "email": "admin@hospital.com",
                    "role": "admin"
                }
            }
            mock_post.return_value = mock_response
            
            # Test 2FA verification
            verification_data = {
                "tempToken": "temp_session_token_for_2fa",
                "code": valid_code
            }
            
            response = requests.post(
                self.verify_2fa_endpoint,
                json=verification_data
            )
            
            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "token" in data
            assert "admin" in data
    
    def test_verify_invalid_2fa_code(self):
        """Test verification with an invalid 2FA code"""
        with patch('requests.post') as mock_post:
            # Mock failed 2FA verification response
            mock
