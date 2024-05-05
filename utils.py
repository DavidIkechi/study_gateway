# utils code.
from password_strength import PasswordPolicy
import datetime
import re
from db.main_model import UserModel
# from db.client_model import RatePlanModel
from exceptions import BadExceptions, NotFoundException, ServerErrorException
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from datetime import datetime as dt
import json




# setup the password policy.
policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 1 uppercase letter
    numbers=1,  # need min. 1 digit
    special=1,# need min. 1 special character
    nonletters=1,  # need min. 1 non-letter characters (digits, specials, anything)
)

# check if the password is an email or not.
def is_password_email(password):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, password) is not None

# for checking password strength.
def check_password(password: str, user: UserModel = None):
    # This returns true or False with the error message.
    error_message = []
    check = True
    pass_check = policy.test(password)
    pass_check = [str(e) for e in pass_check]
    
    if "Length(8)" in pass_check:
        error_message.append("\nPassword must be at least 8 characters long")
        check = False
        
    if "Uppercase(1)" in pass_check:
        error_message.append("\nPassword must include atleast 1 Uppercase character")
        check = False
        
    if "Numbers(1)" in pass_check:
        error_message.append("\nPassword must include atleast 1 Number")
        check = False
        
    if "Special(1)" in pass_check:
        error_message.append("\nPassword must include atleast 1 Special case character")
        check = False
        
    if "Nonletter(1)" in pass_check:
        error_message.append("\nPassword must include atleast 1 Non Character")
        check = False
        
    if not any(char.islower() for char in password):
        error_message.append("\nPassword must include atleast 1 Lowercase Character")
        check = False
    
    if is_password_email(password):
        error_message.append("\nPassword should not be an email address")
        check = False
        
    if user is not None and password.lower() == user.username.lower():
        error_message.append("\nYour Password cannot be your username")
        check = False
        
    return check, ".".join(error_message)
# exclude some fields while outputting
def remove_fields(data, fields):
    if isinstance(data, dict):
        for key in fields:
            data.pop(key, None)
        return {key: remove_fields(value, fields) for key, value in data.items()}
    elif isinstance(data, list):
        return [remove_fields(item, fields) for item in data]
    else:
        return data

def model_to_dict(data):
    data_types = (str, bool, int, datetime.datetime, dict, list, float)

    def convert_value(value):
        if not isinstance(value, data_types):
            return value.__dict__
        return value
    
    return {key: convert_value(value) for key, value in data.items()}

# This function gets the user from the decoded access token.
def get_active_user(db, payload: dict):
    username = payload.get("sub")
    client_id = payload.get("client_id")
    
    return ClientUsers.check_client_username(
        db, client_id, username)
    
# This function updates the paginated dictionary.
def update_dictionary(db, dict_item):
    # get the id.
    id = dict_item.get('id')
    dict_item['active_rate'] = RatePlanModel.create_rate_object(
        db).filter_by(category_id=id, status=True).all()
    dict_item['inactive_rate'] = RatePlanModel.create_rate_object(
        db).filter_by(category_id=id, status=False).all()
    
    return dict_item
        

# This function creates a unique value
def get_unique_value(value):
    time_value = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H%M%S%f')
    return value.lower().replace(" ", "") + time_value

def seed_model (db, model, data, unique_column= ['slug']):
    seeder(db, model, data, unique_column)

def generate_slug(db, value, model, length=10, column_name="slug", pos_right = True):
    # Similar logic as before, but replace 'slug' with column_name
    value = value.ljust(length, '0') if not pos_right else value.rjust(length, '0')
    check_value = db.query(model).filter(getattr(model, column_name) == value).first()
    if check_value:
        raise BadExceptions(f"{column_name}: {value} already exists")

    return value

def seeder(db, model, data, unique_columns:list = []):
    unique_objects = []
    if not unique_columns:
        existing_pairs = []
    else:
        for item in unique_columns:
            new_item = getattr(model, item)
            unique_objects.append (new_item)
        existing_pairs = db.query(*unique_objects).all()
    filtered_data = [d for d in data if (tuple([d[col] for col in unique_columns])) not in existing_pairs]
    instances = [model(**collect) for collect in filtered_data]
    db.add_all(instances)
    db.commit()
    
def paginate_result(model, page, page_size):
    page_offset = Params(page=page, size=page_size)
    return paginate(model, page_offset)

def format_datetime_to_date(date_value):
    """Formats a datetime string as a date string without time information."""
    return dt.strptime(date_value,"%Y-%m-%d").date()