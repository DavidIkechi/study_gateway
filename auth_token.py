#access and refresh token.
from datetime import datetime, timedelta
from jose import jwt
from db.main_model import UserModel
import os

ACCESS_SECRET_KEY = os.getenv('ACCESS_SECRET_KEY')
REFRESH_SECRET_KEY = os.getenv('REFRESH_SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = 10000
REFRESH_TOKEN_EXPIRE_MINUTES = 30

def create_token(users: UserModel):
    # create the access token.
    access_token = create_access_token(users)
    # create the refresh token.
    refresh_token = create_refresh_token(users)
    # todo: generate the page_slug, as well as permission for each users.
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }        

def create_access_token(users: UserModel):
    # Set the expiration time for the access token.
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_expiry = datetime.utcnow() + access_token_expire
        
    access_token_payload = {
        "sub": users.email_address,
        "is_setup": users.is_setup,
        "user_id": users.id,
        "exp": access_token_expiry,
    }
    # encode the token.
    encoded_jwt = jwt.encode(access_token_payload, ACCESS_SECRET_KEY, algorithm="HS256")
    return encoded_jwt
    
def create_refresh_token(users: UserModel):
    # Set the expiration time for the refresh token.
    refresh_token_expire = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token_expiry = datetime.utcnow() + refresh_token_expire
        
    refresh_token_payload = {
        "sub": users.email_address,
        "is_setup": users.is_setup,
        "user_id": users.id,
        "exp": refresh_token_expiry,
    }
    # encode the token.
    encoded_jwt = jwt.encode(refresh_token_payload, REFRESH_SECRET_KEY, algorithm="HS256")
    return encoded_jwt    

def verify_refresh_token(db, token: str):
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=["HS256"]) 
        # get the email and client_id
        email_address = payload.get("sub")
        # get the user model.
        get_user = UserModel.check_email(db, email_address)
        
        new_token = create_token(get_user)
        
    except jwt.ExpiredSignatureError:
        return False, 'Token has expired.'

    except jwt.JWTError:
        return False, "Invalid Token"
    
    except Exception as e:
        return False, str(e)
    
    return True, new_token


def password_verif_token(token):
    try:
        payload = jwt.decode(token, os.getenv('SECRET'), algorithms=['HS256'])
        email:str = payload.get('sub')
        # exp_date: datetime = payload.get('exp')
    except jwt.ExpiredSignatureError:
        return False, 'Token has expired.'

    except jwt.JWTError:
        return False, "Invalid Token"
    
    except Exception as e:
        return False, str(e)
    
    return True, email