import hashlib
import string
from exceptions.exceptions import NewUserError

def new_user_parser(data_dict):
    for k, v in data_dict.items():
        if str(v).strip() == "":
            raise NewUserError(f"Field {k} cannot be empty.")

    password = data_dict.get("password")
    has_upper = any(c.isupper() for c in password) # check for any upper case letters
    has_lower = any(c.islower() for c in password) # check for any lower case letters
    has_digit = any(c.isdigit() for c in password) # check for any digits
    has_special = any(c in string.punctuation for c in password) # check for any special characters
    if not any([has_upper, has_lower, has_digit, has_special]):
        raise NewUserError(f"Password must contain upper letter, lower letter, digit and special character.")

    data_dict['admin'] = True if data_dict['admin'] == 1 else False

    return data_dict