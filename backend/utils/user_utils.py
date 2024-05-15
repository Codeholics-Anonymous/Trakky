from django.core.exceptions import ValidationError
from datetime import datetime, date

def password_validation(password):
    # check if password is alphanumeric
    if (not password.isalnum() or (len(password) < 8) or password.isdigit()):
        return 0
    # check if password contains at least one digit
    contain_digit = False
    for x in password:
        if x.isdigit():
            contain_digit=True
            break
    if not contain_digit:
        return 0
    return 1

def gender_validation(gender):
    if (gender not in ('M', 'F', 'O')):
        raise ValidationError("Incorrect gender")

def date_validation(user_date):
    current_date = date.today()
    if ((user_date > current_date) or ((current_date.year - user_date.year) <= 8)):
        raise ValidationError("Incorrect date")
        