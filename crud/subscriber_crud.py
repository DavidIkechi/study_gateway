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
from db.main_model import SubscriberModel
from argon2 import PasswordHasher
from send_mail import *
from auth_token import *
import pyotp
from datetime import datetime, timedelta
from simpleotp import OTP
import os

def check_mail(db, email, new_user= False):
    get_user = SubscriberModel.check_email(db, email)
    if new_user:
        if get_user is not None:
            raise BadExceptions(detail=f"Email {email} already subscribed.")
    else:
        if get_user is None:
            raise NotFoundException(detail=f"User with this email {email} does not exist.")
        
    return get_user
        

async def create_subscriber(db, user, backtasks):
    # check to see if the email address already exists
    check_subscriber =  check_mail(db, user.email_address, new_user=True)
    # check passwords.
    user_dict = user.dict(exclude_unset = True)
    create_new_subscriber = SubscriberModel.create_subscriber(user_dict)
    db.add(create_new_subscriber)
    # send verification mail notification
    # await send_verification_email(user.email_address, backtasks)
    return create_new_subscriber


async def delete_subscriber(db, email_address, backtasks):
    # check to see if the email address already exists
    check_subscriber =  check_mail(db, email_address)
    
    db.delete(check_subscriber)
    # send verification mail notification
    # await send_verification_email(email_address, backtasks)
    return email_address