import re
from validate_email import validate_email

pass_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$"
name_regex = "^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$"
id_regex = "([0-9]+){7,}$"
phone_number_regex = "^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$"
address_regex = "^[#.0-9a-zA-Z\s,-]+$"
F_ACTIVE = 'ACTIVE'
F_INACTIVE = 'INACTIVE'
EMAIL_APP = 'EMAIL_APP'
REQ_ACTIVATE = 'REQ_ACTIVATE'
REQ_FORGOT = 'REQ_FORGOT'
U_UNCONFIRMED = 'UNCONFIRMED'
U_CONFIRMED = 'CONFIRMED'


def isEmailValid(email):
    is_valid = validate_email(email)
    return is_valid


def isNameValid(name):
    if re.search(name_regex, name):
        return True
    else:
        return False


def isId_NumberValid(id_number):
    if re.search(id_regex, id_number):
        return True
    else:
        return False


def isAddressValid(address):
    if re.search(address_regex, address):
        return True
    else:
        return False


def isPhone_numberValid(phone_number):
    if re.search(phone_number_regex, phone_number):
        return True
    else:
        return False


def isPasswordValid(password):
    if re.search(pass_regex, password):
        return True
    else:
        return False
