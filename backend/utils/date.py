from datetime import datetime, date
from django.core.validators import ValidationError

def calculate_days_difference(starting_date, ending_date):
    if isinstance(starting_date, str):
        starting_date = datetime.strptime(starting_date, "%Y-%m-%d").date()
    if isinstance(ending_date, str):
        ending_date = datetime.strptime(ending_date, "%Y-%m-%d").date()
    return (ending_date - starting_date).days + 1

def date_validation(starting_date, ending_date = date.today()):
    if (starting_date > ending_date):
        raise ValidationError("Incorrect date")

def calculate_age(birth_date):
    current_date = date.today()
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
    return current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))

def age_validation(birth_date):
    today = date.today()
    age = calculate_age(birth_date)
    if (age < 12):
        raise ValidationError("Birth date is incorrect.")