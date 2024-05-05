import sys
sys.path.append("..")
from utils import *
from db.session import Session
from sqlalchemy.orm import Session, load_only, relationship
from exceptions import BadExceptions, NotFoundException, ServerErrorException, NotAuthorizedException
from db.main_model import UserModel
from argon2 import PasswordHasher

hasher = PasswordHasher()

def check_email(db, email, new_user= False):
    get_user = UserModel.check_email(db, email)
    if new_user:
        if get_user is not None:
            raise BadExceptions(detail=f"Email {email} already in use.")
    else:
        if get_user is None:
            raise NotFoundException(detail=f"User with this email {email} does not exist.")
        
    return get_user
        

def create_user(db, user):
    # check to see if the email address already exists
    check_user =  check_email(db, user.email_address, new_user=True)
    # check passwords.
    get_password = user.password
    if get_password is "":
        raise BadExceptions(detail="Password cannot be blank.")
    
    if get_password != user.confirm_password:
        raise BadExceptions(detail="Password do not match.")
    
    bool, message = check_password(get_password)
    if not bool:
        raise BadExceptions(detail=message)
    
    user_dict = user.dict(exclude_unset = True)
    user_dict['password'] = hasher.hash(user_dict['password'])
    
    user_dict.pop('confirm_password')
    
    create_new_user = UserModel.create_user(user_dict)
    db.add(create_new_user)
    # send verification mail notification
    
    return create_new_user
