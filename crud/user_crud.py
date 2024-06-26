import sys
sys.path.append("..")
from utils import *
from db.session import Session
from sqlalchemy.orm import Session, load_only, relationship
from exceptions import (
    BadExceptions, 
    NotFoundException, 
    ServerErrorException, 
    NotAuthorizedException,
    ForbiddenException
)
from db.main_model import UserModel
from argon2 import PasswordHasher
from send_mail import *
from auth_token import *
import pyotp
from datetime import datetime, timedelta
from simpleotp import OTP
import os

hasher = PasswordHasher()

def check_user_account(user: UserModel):
    if not user.status:
        raise exceptions.bad_request_error("Account is disabled")
    # check if the user's account is verified or not.
    if not user.is_verified:
        raise ForbiddenException(detail="Sorry, user's account is not verified")
    # checked if password is locked here.
    if user.is_lock:
        raise ForbiddenException(detail="Sorry, user's account is locked")

    return True

def check_mail(db, email, new_user= False):
    get_user = UserModel.check_email(db, email)
    if new_user:
        if get_user is not None:
            raise BadExceptions(detail=f"Email {email} already in use.")
    else:
        if get_user is None:
            raise NotFoundException(detail=f"User with this email {email} does not exist.")
        
    return get_user

async def create_user(db, user, backtasks):
    from crud.user_profile_crud import create_user_profile
    # check to see if the email address already exists
    check_user =  check_mail(db, user.email_address, new_user=True)
    # check passwords.
    get_password = user.password
    if get_password == "":
        raise BadExceptions(detail="Password cannot be blank.")
    
    if get_password != user.confirm_password:
        raise BadExceptions(detail="Password do not match.")
    
    bool, message = check_password(get_password)
    if not bool:
        raise BadExceptions(detail=message)
    
    user_dict = user.dict(exclude_unset = True)
    user_dict['password'] = hasher.hash(user_dict['password'])
    user_dict['code'] = pyotp.random_base32()
    # user_dict['is_verified'] = True
    user_dict.pop('confirm_password')
    
    create_new_user = UserModel.create_user(user_dict)
    db.add(create_new_user)
    db.flush()
    # create new user profile immediately.
    _ = create_user_profile(db, create_new_user.id)
    # send verification mail notification
    await send_verification_email(create_new_user, backtasks)
    
    return create_new_user

def user_login(db, email, password):
    # first check if email_address exists.
    check_user = check_mail(db, email)
    # check email and password combo.
    if hasher.verify(check_user.password, password):
        # check if the user's account is active or not.
        _ = check_user_account(check_user)
        # reset password lock on successful login.
        # _ = set_lock(db, check_user, logged_in = True)
        get_token = create_token(check_user)
        # increase the login count and also adjust last login.
        check_user.login_count += 1
        check_user.last_login = datetime.utcnow()
        
    return get_token

async def send_code(db, email: str, backtasks):
    # first check if email_address exists.
    check_user = check_mail(db, email)
    _ = check_user_account(check_user)

    SECRET_KEY = os.getenv('SECRET')

    otp_handler = OTP(SECRET_KEY,
                  length=6,
                  expires_after=15,
                  user_identifier=check_user.email_address)

    # generate OTP - returns OTP and hash
    sent_code, sig = otp_handler.generate()
    # send verification code notification
    await send_verification_code(check_user, sent_code, backtasks)
    check_user.code = sig

    return check_user


def verify_code(db, code):
     # first check if email_address exists.
    check_user = check_mail(db, code.email_address)
    SECRET_KEY = os.getenv('SECRET')

    otp_handler = OTP(SECRET_KEY,
                  length=6,
                  expires_after=15,
                  user_identifier=check_user.email_address)

    get_token = generate_verification_token(code.email_address)


    _ = check_user_account(check_user)

    secret_key = check_user.code
    is_verified = otp_handler.verify(code.otp, secret_key)

    
    if not (is_verified):
        raise BadExceptions(detail="Invalid One-Time Password or expired code")

    return get_token

def change_password(db, token, user):
    # check to see if the email address already exists
    check_user =  check_mail(db, user.email_address)
    _ = check_user_account(check_user)

    # decode token.
    bool_result, token_data = password_verif_token(token)

    if not bool_result:
        raise BadExceptions(token_data) 

    if token_data != check_user.email_address:
        raise BadExceptions(f"Token email doesn't match with email supplied.")
    # check passwords.
    get_password = user.password
    if get_password == "":
        raise BadExceptions(detail="Password cannot be blank.")
    
    if get_password != user.confirm_password:
        raise BadExceptions(detail="Password do not match.")
    
    bool, message = check_password(get_password)
    if not bool:
        raise BadExceptions(detail=message)
    
    check_user.password = hasher.hash(user.password)
    
    return check_user

def refresh_token(db, token):
    bool_result, token_data = verify_refresh_token(db, token)
        
    if not bool_result:
        raise BadExceptions(token_data)
    
    return token_data

async def resend_link(db, user, backtasks):
    # check to see if the email address already exists
    check_user =  check_mail(db, user.email_address)

    if check_user.is_verified:
        raise BadExceptions(detail="Account already verified")
    # send verification mail notification
    await send_verification_email(user, backtasks)
    
    return check_user

async def verify_token(db, token, backtask):
    # decode token.
    bool_result, token_data = password_verif_token(token)

    if not bool_result:
        raise BadExceptions(token_data)

    check_user =  check_mail(db, token_data)
    if check_user.is_verified:
        raise BadExceptions(detail="Account already verified")
    
    await welcome_email(check_user, backtask)
    check_user.is_verified = True
    
    return check_user

def get_user_by_email(db, email_address):
    get_email = check_mail(db, email_address)
    return UserModel.get_user_by_email(db, email_address)

def get_user_detail(db, user_dict):
    email_address = user_dict.get('sub')
    return get_user_by_email(db, email_address)