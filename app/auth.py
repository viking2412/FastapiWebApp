import jwt
import bcrypt
from datetime import UTC, datetime, timedelta

SECRET_KEY = "your_secret_key"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def create_token(user_id: int) -> str:
    payload = {"sub": str(user_id), "exp": datetime.now(tz=UTC) + timedelta(hours=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return int(payload["sub"])
    except (jwt.ExpiredSignatureError, jwt.DecodeError, ValueError):
        return None
