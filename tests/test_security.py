from datetime import datetime, timedelta, timezone

import jwt
import pytest

from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.core.config import get_settings

settings = get_settings()

def test_hash_password_returns_different_hashes():
    password = "password"

    hash1 = hash_password(password=password)
    hash2 = hash_password(password=password)

    assert hash1 != hash2

def test_verify_password_correct():
    password = "password"
    hash = hash_password(password)

    result = verify_password(password=password, hashed_password=hash)
    assert result

def test_verify_password_wrong():
    password1 = "wrongpassword"
    password2 = "correctpassword"

    hash = hash_password(password2)

    result = verify_password(password=password1, hashed_password=hash)
    assert result is False

def test_token_roundtrip():
    user_id = "user-5"

    token = create_access_token(user_id=user_id)
    decode_token = decode_access_token(token=token)

    assert user_id == decode_token

def test_decode_forged_token():
    user_id = "user-5"

    token = create_access_token(user_id=user_id)
    with pytest.raises(jwt.InvalidSignatureError):
        decode_access_token(token=token+"x")

def test_decode_expired_token():
    user_id = "user-5"

    payload = {"sub": user_id, "exp": datetime.now(timezone.utc) - timedelta(minutes=1)}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(token=token)