from datetime import timedelta
import time
from app.core.auth_utils import get_password_hash, verify_password, create_access_token, decode_token

def test_password_hashing():
    password = "secret_password"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

def test_jwt_token_flow():
    payload = {"sub": "shreya_yadav", "role": "developer"}
    
    # Create token
    token = create_access_token(payload, expires_delta=timedelta(minutes=5))
    assert isinstance(token, str)
    
    # Decode token
    decoded = decode_token(token)
    assert decoded is not None
    assert decoded["sub"] == "shreya_yadav"
    assert decoded["role"] == "developer"

def test_expired_token():
    payload = {"sub": "shreya_yadav"}
    # Create token expiring in negative time
    token = create_access_token(payload, expires_delta=timedelta(seconds=-10))
    
    decoded = decode_token(token)
    assert decoded is None
