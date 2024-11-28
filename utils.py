import jwt
import dbhandler as dbhandler
from main import dbclient
import os

SecretKey = os.getenv("JWT_SECRET")


def create_token(data: dict):
    return jwt.encode(data, SecretKey, algorithm="HS256")

def decode_token(token):
    return jwt.decode(token, SecretKey, algorithms=["HS256"])

def get_user(token):
    try:
        decoded = decode_token(token)
        email = decoded["email"]
        return dbhandler.get_user(dbclient,email)
    except Exception as e:
        return None
    
def validateChannel(channel_id,email):
    channel = dbhandler.get_channel(dbclient,channel_id)
    if channel:
        return email in channel.get("emails", [])
    return False